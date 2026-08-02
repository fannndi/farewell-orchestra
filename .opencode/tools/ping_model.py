#!/usr/bin/env python3
"""Pre-dispatch ping: check if a model alias is reachable via 9router proxy.

Reads live config from opencode.jsonc (NOT profiles.json). Strips leading
"9router/" prefix before sending to the proxy (which 404s with it).
"""
import json, sys, os, argparse, urllib.request, urllib.error

DEFAULT_CONFIG = os.path.join(
    os.path.dirname(__file__), "..", "..", "opencode.jsonc"
)
DEFAULT_BASE = "http://127.0.0.1:20128/v1"


def load_jsonc(path):
    """Load JSONC — strip // line-comments only when outside quotes."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    out = []
    in_string = False
    escape = False
    i = 0
    while i < len(text):
        ch = text[i]
        if escape:
            out.append(ch)
            escape = False
            i += 1
            continue
        if ch == '\\' and in_string:
            out.append(ch)
            escape = True
            i += 1
            continue
        if ch == '"':
            in_string = not in_string
            out.append(ch)
            i += 1
            continue
        if not in_string and ch == '/' and i + 1 < len(text) and text[i + 1] == '/':
            # skip to end of line
            while i < len(text) and text[i] != '\n':
                i += 1
            continue
        out.append(ch)
        i += 1
    return json.loads("".join(out))


def main():
    parser = argparse.ArgumentParser(description="Ping a model via 9router proxy")
    parser.add_argument(
        "--agent",
        required=True,
        choices=["orchestrator", "executor", "researcher", "reviewer"],
    )
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    args = parser.parse_args()

    try:
        cfg = load_jsonc(args.config)
    except Exception:
        print("DEAD")
        sys.exit(1)

    # Resolve model alias
    agents = cfg.get("agent", {})
    agent = agents.get(args.agent)
    if not agent:
        print("DEAD")
        sys.exit(1)
    alias = agent.get("model")
    if not alias:
        print("DEAD")
        sys.exit(1)

    # Resolve base URL
    providers = cfg.get("provider", {})
    nine = providers.get("9router", {})
    base_url = nine.get("options", {}).get("baseURL", DEFAULT_BASE)

    # Strip leading "9router/" prefix — proxy expects bare alias
    if alias.startswith("9router/"):
        alias = alias[len("9router/"):]

    url = f"{base_url}/chat/completions"
    payload = json.dumps({
        "model": alias,
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 10,
    }).encode("utf-8")

    headers = {"Content-Type": "application/json"}
    api_key = os.environ.get("NINEROUTER_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read()
            # Proxy may append SSE "data: [DONE]" after JSON — use raw_decode
            decoder = json.JSONDecoder()
            data, _ = decoder.raw_decode(raw.decode("utf-8"))
            choices = data.get("choices", [])
            if choices:
                msg = choices[0].get("message", {})
                # Reasoning-only models put output in "reasoning", not "content"
                if msg.get("content") or msg.get("reasoning"):
                    print("ALIVE")
                    sys.exit(0)
            print("DEAD")
            sys.exit(1)
    except Exception:
        print("DEAD")
        sys.exit(1)


if __name__ == "__main__":
    main()
