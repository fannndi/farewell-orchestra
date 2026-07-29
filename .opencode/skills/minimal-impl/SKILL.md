---
name: minimal-impl
description: Use before writing code — YAGNI ladder, verify-first, cleanup, error healing
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

## Error Healing — Priority Order

Kalau kode error setelah implementasi, TANYAIN ke diri sendiri:

1. **Typo / import / syntax?** → fix langsung tanpa diskusi.
2. **Timeout / rate limit?** → 1x retry: kurangi `max_tokens` 30%, sederhanakan prompt. Kalau tetap timeout → report "TIMEOUT after retry" — jangan escalate ke orchestrator, cukup catat di report.
3. **Tool call malformed?** (salah argumen, missing field, wrong type) → baca error message, perbaiki argumen, retry 1x. Kalau gagal lagi → STOP, report "TOOL_FAIL" dengan detail error.
4. **Tool not found / permission denied?** → STOP langsung. Eskalasi ke orchestrator. Jangan retry.
5. **Logic error** (output nggak sesuai expected) → 1x retry dengan asumsi berbeda. Kalau gagal lagi → STOP, laporkan diff.
6. **Structural error** (framework/library, perlu arsitektur ulang) → **STOP. >2x = eskalasi.** Laporkan detail ke orchestrator.

**Prinsip:** timeout + tool fail ringan = retry 1x trus jalan. Tool not found + permission denied = STOP. Struktural >2x = eskalasi.

## Report Format

```
Done. X file(s) changed.
Verification: [command output — 1 line]
Deviation: [only if berbeda dari brief] — skip if none.
```

**Jangan:** cerita proses, justifikasi, "I also noticed...", saran tambahan.
