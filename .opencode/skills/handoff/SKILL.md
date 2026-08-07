---
name: handoff
description: Compact conversation into handoff document for session continuity.
activation: When session ends
trigger: Session end OR context >80% full OR task done OR blocker found
---

# Handoff

Compact current conversation into handoff document. Another agent can continue work.

## Trigger

- Session即将结束
- Context window almost full
- Switching to different task
- User asks for handoff

## Format

```markdown
# Handoff: [task name]

## Status
[IN_PROGRESS/BLOCKED/DONE]

## What Was Done
- [step 1]
- [step 2]

## What's Left
- [ ] [remaining task 1]
- [ ] [remaining task 2]

## Decisions Made
- [decision 1] — [reason]
- [decision 2] — [reason]

## Blockers
- [blocker 1] — [status]

## Key Files
- [file 1] — [purpose]
- [file 2] — [purpose]

## Next Steps
1. [immediate next step]
2. [following step]
```

## Rules

1. **Compact** — max 1 page
2. **Actionable** — next steps harus spesifik
3. **Context** — include enough untuk resume
4. **Decisions** — catat kenapa keputusan diambil

## Contoh

```markdown
# Handoff: Tambahin fitur login

## Status
IN_PROGRESS

## What Was Done
- Research existing auth setup
- Implement JWT authentication
- Add login endpoint

## What's Left
- [ ] Add rate limiting
- [ ] Add refresh token
- [ ] Write tests

## Decisions Made
- Pakai JWT, bukan session — lebih scalable
- 24h expiry — balance security dan UX

## Key Files
- src/auth.ts — auth module
- src/auth.test.ts — tests

## Next Steps
1. Add rate limiting ke /login endpoint
2. Add refresh token mechanism
3. Write integration tests
```

## Cross-Project Handoff

Kalau handoff melibatkan project lain:

### Additional Fields
```markdown
## Project Context
- **Project Path:** [absolute path]
- **Project Type:** [Flutter/Node/Python/Rust/Go]
- **Tech Stack:** [framework, language, packages]
- **Docs Status:** [5/5 core, 3/5 core, etc.]

## Permission Status
- [ ] Path di external_directory
- [ ] Sub-agents bisa akses
- [ ] Executor punya bash commands

## Session Memory
- sub-project.md updated? [yes/no]
- Agent memory updated? [yes/no]
```

### Handoff Checklist
- [ ] sub-project.md updated dengan latest context
- [ ] Agent memory updated (1 baris per agent)
- [ ] Decisions documented
- [ ] Next steps spesifik
- [ ] Permission status documented

## Auto-Handoff Triggers

1. Context window > 80% full
2. Session > 30 menit
3. Task selesai → report + handoff
4. Blocker ditemukan → handoff dengan blocker info

**Pemicu:** Context >80% dideteksi context-window skill (bukan self-detect). Urutan: compress dulu, handoff kalau masih penuh.

## Handoff File Location

Save handoff to:
```
<project>/docs/handoff-<date>.md
```

Or if no docs directory:
```
<project>/HANDOFF.md
```
