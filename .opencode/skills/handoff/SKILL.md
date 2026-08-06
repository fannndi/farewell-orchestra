---
name: handoff
description: Compact conversation into handoff document for session continuity.
activation: When session ends
trigger: Session????
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
