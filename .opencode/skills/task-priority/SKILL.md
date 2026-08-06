---
name: task-priority
description: Prioritize tasks based on impact and urgency.
activation: When multiple tasks
trigger: Multiple tasks
---

# Task Priority

Prioritaskan task berdasarkan impact dan urgency.

## Priority Matrix

| | High Impact | Low Impact |
|---|---|---|
| **High Urgency** | P1 — Do First | P2 — Schedule |
| **Low Urgency** | P3 — Delegate | P4 — Drop |

## Priority Rules

### P1 — Do First
- Production bugs
- Security vulnerabilities
- Data loss risk
- Blocking other work

### P2 — Schedule
- Feature requests
- Performance improvements
- Technical debt
- Documentation

### P3 — Delegate
- Simple fixes
- Routine tasks
- Repetitive work
- Low complexity

### P4 — Drop
- Nice-to-have
- Speculative
- Low value
- High effort, low return

## Decision Tree

```
Task masuk
  │
  ▼
Apakah blocking production?
  ├── Ya → P1
  └── Tidak
        │
        ▼
      Apakah ada deadline?
        ├── Ya → P2
        └── Tidak
              │
              ▼
            Apakah complexity rendah?
              ├── Ya → P3
              └── Tidak → P4
```

## Rules

1. **Impact first** — high impact > high urgency
2. **Delegate** — low complexity → delegate ke executor
3. **Drop** — low value → drop atau defer
4. **Review** — review priority setiap session

## Integration

- Orchestrator assign priority setiap task
- Priority menentukan urutan eksekusi
- Priority bisa berubah berdasarkan context

## Contoh

```markdown
## Task Queue

### P1 — Do First
- [ ] Fix login bug (production down)
- [ ] Patch security vulnerability

### P2 — Schedule
- [ ] Add user dashboard
- [ ] Optimize database queries

### P3 — Delegate
- [ ] Update documentation
- [ ] Fix typo in UI

### P4 — Drop
- [ ] Add animation effects
- [ ] Refactor working code
```
