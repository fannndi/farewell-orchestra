---
name: session-state
description: Track session progress and state across interactions.
---

# Session State

Track apa yang terjadi di session ini. Bantu LLM understand context.

## State Format

```markdown
# Session State

## Current Task
[deskripsi task yang sedang dikerjakan]

## Progress
- [x] Step 1: [apa yang sudah dilakukan]
- [ ] Step 2: [apa yang akan dilakukan]

## Context
- Files yang sudah diubah: [list]
- Decisions yang sudah diambil: [list]
- Blockers yang ada: [list]

## Memory
- [info penting yang perlu diingat]
```

## Rules

1. **Update setiap step** — jangan tunggu selesai
2. **Catat decisions** — kenapa keputusan diambil
3. **Catat blockers** — apa yang menghambat
4. **Catat files** — file apa saja yang sudah diubah

## Integration

- Orchestrator update session state setiap step
- Sub-agents bisa baca session state untuk context
- Session state di-reset setiap session baru

## Contoh

```markdown
# Session State

## Current Task
Tambahin fitur login ke app

## Progress
- [x] Step 1: Research existing auth — DONE
- [x] Step 2: Review security — DONE
- [ ] Step 3: Implement login — IN_PROGRESS
- [ ] Step 4: Verify — PENDING

## Context
- Files: src/auth.ts, src/auth.test.ts
- Decisions: Pakai JWT, bukan session
- Blockers: (none)

## Memory
- Auth module sudah ada, tinggal tambahin login endpoint
- JWT expiry 24 jam
```
