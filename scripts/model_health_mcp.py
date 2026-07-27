"""MCP Server: Model Health Check via 9Router Gateway.
Exposes tools for pre-flight model health checking before AI agent dispatch.
"""
import json, time, sys, os
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import httpx

NINEROUTER_URL = os.environ.get("NINEROUTER_URL", "http://127.0.0.1:20128/v1")
NINEROUTER_API_KEY = os.environ.get("NINEROUTER_API_KEY", "")

# Free models we care about (from farewell-orchestra profiles)
FREE_MODELS = [
    "oc/north-mini-code-free",
    "oc/nemotron-3-ultra-free",
]

HEALTH_TIMEOUT = 15.0  # seconds for health check request

app = Server("model-health-mcp")

async def _ping_model(model: str) -> dict:
    """Send minimal completion to model via 9Router. Returns {ok, latency_ms, error}."""
    headers = {"Content-Type": "application/json"}
    if NINEROUTER_API_KEY:
        headers["Authorization"] = f"Bearer {NINEROUTER_API_KEY}"
    
    body = {
        "model": model,
        "messages": [{"role": "user", "content": "hi"}],
        "max_tokens": 1,
        "stream": False,
    }
    
    t0 = time.time()
    try:
        async with httpx.AsyncClient(timeout=HEALTH_TIMEOUT) as client:
            resp = await client.post(
                f"{NINEROUTER_URL}/chat/completions",
                json=body,
                headers=headers,
            )
        latency_ms = int((time.time() - t0) * 1000)
        resp.raise_for_status()
        data = resp.json()
        ok = "choices" in data and len(data["choices"]) > 0
        return {"ok": ok, "latency_ms": latency_ms, "error": None if ok else "no choices in response"}
    except httpx.TimeoutException:
        return {"ok": False, "latency_ms": int((time.time() - t0) * 1000), "error": "timeout"}
    except httpx.HTTPStatusError as e:
        return {"ok": False, "latency_ms": int((time.time() - t0) * 1000), "error": f"HTTP {e.response.status_code}"}
    except Exception as e:
        return {"ok": False, "latency_ms": int((time.time() - t0) * 1000), "error": str(e)[:200]}
    

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="model_health",
            description="Check health & latency of free AI models via 9Router. Use BEFORE dispatching agents to avoid streaming failures.",
            inputSchema={
                "type": "object",
                "properties": {
                    "models": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": f"Model IDs to check. Default: {FREE_MODELS}"
                    }
                }
            }
        ),
        Tool(
            name="model_warmup",
            description="Send a warm-up ping to a model to reduce cold-start latency. Use at session start for free models.",
            inputSchema={
                "type": "object",
                "properties": {
                    "model": {
                        "type": "string",
                        "description": "Model ID to warm up, e.g. oc/north-mini-code-free"
                    }
                },
                "required": ["model"]
            }
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "model_health":
        models = arguments.get("models", FREE_MODELS)
        results = {}
        for m in models:
            r = await _ping_model(m)
            results[m] = r
        
        # Format output
        lines = []
        healthy = sum(1 for r in results.values() if r["ok"])
        lines.append(f"=== Model Health ({healthy}/{len(results)} OK) ===")
        for m, r in results.items():
            status = "✅ OK" if r["ok"] else "❌ FAIL"
            err = f" — {r['error']}" if r["error"] else ""
            lines.append(f"  {status} | {m:35s} | {r['latency_ms']:5d}ms{err}")
        
        lines.append("")
        if healthy == 0:
            lines.append("⚠️  ALL MODELS DOWN — streaming will fail. Consider switching profile.")
        elif healthy < len(results):
            lines.append(f"⚠️  {len(results) - healthy} model(s) down. Orchestrator should use only healthy models.")
        else:
            best = min(results.items(), key=lambda x: x[1]["latency_ms"])
            lines.append(f"💡 Recommended: {best[0]} ({best[1]['latency_ms']}ms) — fastest response.")
        
        return [TextContent(type="text", text="\n".join(lines))]
    
    elif name == "model_warmup":
        model = arguments["model"]
        r = await _ping_model(model)
        if r["ok"]:
            return [TextContent(type="text", text=f"✅ {model} warmed up ({r['latency_ms']}ms)")]
        else:
            return [TextContent(type="text", text=f"❌ {model} warm-up failed: {r['error']}")]
    
    return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
