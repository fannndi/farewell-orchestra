---
name: status
description: Show orchestration health — agent status, model, token usage, uptime
---

# /status — Orchestration Health Check

Display real-time status of the orchestra system.

## Output Format

```jsonc
{
  "timestamp": "2026-07-28T13:45:00Z",
  "profile": "hybrid",
  "agents": {
    "orchestrator": { "model": "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free", "steps_used": 12, "steps_limit": 25, "status": "active" },
    "researcher":  { "model": "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free", "steps_used": 8,  "steps_limit": 22, "status": "idle" },
    "reviewer":    { "model": "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free", "steps_used": 5,  "steps_limit": 20, "status": "idle" },
    "executor":    { "model": "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free", "steps_used": 0,  "steps_limit": 25, "status": "idle" }
  },
  "tokens": { "used": 12400, "limit": 1000000, "pct": 1 },
  "uptime_seconds": 3600,
  "active_project": "farewell-orchestra"
}
```

## Health Thresholds

| Metric | Warn | Critical |
|--------|------|----------|
| Token usage | > 50% | > 80% |
| Steps used | > 70% limit | > 90% limit |
| Uptime | > 4 hours | > 8 hours |
| Active project | missing | missing |

## Exit Codes

- `0` — Healthy
- `1` — Warning (token or step usage high)
- `2` — Critical (token/step limit approaching, no active project)
