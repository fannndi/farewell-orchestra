---
name: context-manager
description: Context prioritization. Manage context across sessions.
activation: When context full
trigger: Context window full
---

# Context Manager

Context prioritization. Manage context across sessions.

## Context Priority

| Priority | Context | Keep | Drop |
|----------|---------|------|------|
| 1 (Critical) | Current task, blockers | Always | Never |
| 2 (High) | Recent decisions, active context | Usually | Only if full |
| 3 (Medium) | Historical context | Sometimes | If not relevant |
| 4 (Low) | Old sessions, completed tasks | Rarely | Usually |

## Context Management

### When Context is Full
1. Drop Low priority first
2. Then Medium priority
3. Keep High and Critical

### When Context is Empty
1. Load Critical from sub-project.md
2. Load High from recent memory
3. Load Medium from lessons
4. Skip Low

## Context Format

```markdown
## Context (Priority: [level])

### Critical
- Current task: [deskripsi]
- Blockers: [list]

### High
- Recent decisions: [list]
- Active context: [deskripsi]

### Medium
- Historical: [ringkasan]

### Low
- Old sessions: [ringkasan]
```

## Rules

1. **Prioritize** — Critical > High > Medium > Low
2. **Compress** — Ringkaskan, jangan copy paste
3. **Update** — Refresh setiap step
4. **Drop** — Hapus yang tidak relevan

## Integration

- Orchestrator manage context setiap step
- Sub-agents dapat context sesuai priority
- Context manager drop context kalau penuh

## Contoh

**Before (penuh):**
```
Context: 5000 tokens
- Task A details (500 tokens)
- Task B details (500 tokens)
- Old session 1 (1000 tokens)
- Old session 2 (1000 tokens)
- Current task (500 tokens)
- Blockers (100 tokens)
- Decisions (400 tokens)
- Historical (1000 tokens)
```

**After (compressed):**
```
Context: 2000 tokens
- Current task (500 tokens) — Critical
- Blockers (100 tokens) — Critical
- Decisions (400 tokens) — High
- Historical summary (200 tokens) — Medium
- Old sessions: [compressed] (800 tokens) — Low
```
