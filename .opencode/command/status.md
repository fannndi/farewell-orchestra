---
name: status
description: Show orchestration health — agent model, profile, sensor coverage
---

# /status — Orchestration Health Check

Display real-time health of the orchestra system.

## Usage

Panggil via orchestrator: `@harness_status check:"all" format:"json"`

## Output Schema (format:json)

```jsonc
{
  "timestamp": "2026-07-30T13:45:00Z",
  "active_project": "farewell-orchestra",
  "profile": "9router/ocg/deepseek-v4-flash",
  "small_model": "9router/oc/north-mini-code-free",
  "agents": {
    "orchestrator": { "model": "ocg/deepseek-v4-flash", "steps_limit": 22 },
    "researcher":  { "model": "north-mini-code-free",    "steps_limit": 24 },
    "reviewer":    { "model": "nemotron-3-ultra-free",   "steps_limit": 20 },
    "executor":    { "model": "nemotron-3-ultra-free",   "steps_limit": 25 }
  },
  "profiles": {
    "total": 6,
    "valid": true,
    "names": ["default-oc", "default-or", "codex-oc", "codex-or", "ollama-oc", "ollama-or"]
  },
  "sensors": {
    "ok": 12,
    "missing": 3,
    "partial": 4
  },
  "errors": null,
  "healthy": true
}
```

## Fields

| Field | Source | Notes |
|-------|--------|-------|
| `timestamp` | Tool runtime | ISO 8601 |
| `profile` | opencode.jsonc `model` | Active model ID |
| `agents.*.model` | opencode.jsonc `agent.*.model` | Short model ID (no provider prefix) |
| `agents.*.steps_limit` | opencode.jsonc `agent.*.steps` | Declared step budget |
| `profiles.valid` | `generate.py --validate` exit code | |
| `sensors.*` | LESSONS.md ## Sensor Coverage | Count of ✅❌⚠️ |

## Health

- `healthy: true` — no errors
- `healthy: false` + `errors: [...]` — something wrong

## Exit Codes (CLI)

- `0` — Healthy
- `1` — Warning
- `2` — Critical
