---
name: minimal-impl
description: Minimal implementation — YAGNI-first, verify-before-report, delete-over-add, budget-aware
---

# Minimal Implementation

Boss bayar per token DAN per tool call. Setiap byte kode harus justified.

## YAGNI Ladder (top = cheapest, start from top)

1. **Does this need to exist?** → No? Stop. Delete.
2. **Stdlib does it?** → Use it.
3. **Platform covers it?** → CSS over JS. DB constraint over app code.
4. **Existing dep solves it?** → Use it. **NEVER add new dep.**
5. **One line?** → One line.
6. **Only then:** minimum code that works. Delete > add. Boring > clever.

## Budget Rules

- **Read files ONLY if needed.** Brief kasih file+line → langsung ke sana.
- **Prefer delete over add.** Menghapus 5 baris > menambah 3 baris.
- **Satu change per edit.** Jangan batch unrelated fixes.
- **Verification:** EXACT command dari brief. Jangan nambah check.
- **Never announce tool calls.** Jangan bilang "I will now..." — just do.

## Not-Lazy Guard

JANGAN PERNAH menyederhanakan:
- Input validation di trust boundary
- Error handling yang mencegah data loss
- Security (auth, encryption, sanitization)
- Accessibility
- Apapun yang Boss explicitly minta

## Precision

- **Typo = reject.** Diff-check setiap identifier.
- **Duplication >2x** → extract. Don't Repeat Yourself.
- **No premature abstraction:** jangan bikin interface kalau cuma 1 implementasi.
- **Follow existing file style.** Jangan campur snake_case/camelCase.

## Cleanup Before Report

- Hapus unused imports, dead variables, dead comments
- Hapus console.log, breakpoints, debug prints
- Cek naming consistency dengan file yang diedit

## DoD — Definition of Done

- [ ] Verification passes (per brief)
- [ ] Zero broken references
- [ ] No TODO/FIXME introduced
- [ ] Diff matches scope — no extra files
- [ ] Naming consistent
- [ ] Lint clean

## Error Healing

Kalau kode error setelah implementasi:

1. **Simple fix** — typo, missing import, wrong variable name → perbaiki sendiri. Jangan tanya Boss.
2. **Logic error** — salah algoritma, output nggak sesuai expected → 1x retry dengan asumsi berbeda.
3. **Structural error** — error dari framework/library, perlu arsitektur ulang → **STOP. Jangan coba >2x.** Laporkan ke orchestrator dengan detail error. Researcher akan dipanggil buat deep debugging.

**Prinsip:** error kecil = tanggung jawab lo. Error besar = jangan buang token, eskalasi.

## Report Format

```
Done. X file(s) changed.
Verification: [command output — 1 line]
Deviation: [only if berbeda dari brief] — skip if none.
```

**Jangan:** cerita proses, justifikasi, "I also noticed...", saran tambahan.
