---
name: progress-tracker
description: Persistent task tracking. Track progress across sessions.
activation: After task completion
trigger: Task selesai
---

# Progress Tracker

Persistent task tracking. Track progress across sessions.

## Format

```markdown
# Task: [nama task]

## Status: [IN_PROGRESS/BLOCKED/DONE]

## Progress
- [x] Step 1: [deskripsi]
- [x] Step 2: [deskripsi]
- [ ] Step 3: [deskripsi] — BLOCKED: [alasan]
- [ ] Step 4: [deskripsi]

## Decisions
- [tanggal] [keputusan] — [alasan]

## Blockers
- [tanggal] [blocker] — [status]

## Notes
- [catatan penting]
```

## Rules

1. **Update setiap step** — jangan tunggu selesai
2. **Catat decisions** — kenapa keputusan diambil
3. **Catat blockers** — apa yang menghambat
4. **Resume dari last state** — jangan mulai dari nol

## Integration

- Orchestrator update progress tracker setiap step
- Sub-agents bisa baca progress tracker untuk context
- Boss bisa baca progress tracker untuk status

## Contoh

```markdown
# Task: Tambahin fitur login

## Status: IN_PROGRESS

## Progress
- [x] Step 1: Research existing auth — DONE
- [x] Step 2: Review security — DONE
- [ ] Step 3: Implement login — IN_PROGRESS
- [ ] Step 4: Verify — PENDING

## Decisions
- [2026-08-06] Pakai JWT, bukan session — lebih scalable

## Blockers
- (none)

## Notes
- Auth module sudah ada, tinggal tambahin login endpoint
```
