---
name: minimal-impl
description: Use before writing code — YAGNI ladder, verify-first, cleanup, error healing.
---

> Role: executor — write access, implement before verify. Orchestrator never writes code.

# Minimal Implementation

Setiap byte kode harus justified.

## YAGNI Ladder

1. **Does this need to exist?** → No? Stop. Delete.
2. **Stdlib does it?** → Use it.
3. **Platform covers it?** → CSS over JS. DB constraint over app code.
4. **Existing dep solves it?** → Use it. **NEVER add new dep.**
5. **One line?** → One line.
6. **Only then:** minimum code that works. Delete > add. Boring > clever.

## Budget Rules

- **Read files ONLY if needed.** Langsung ke file+line.
- **Prefer delete over add.** Hapus 5 > tambah 3.
- **Satu change per edit.** Jangan batch. **Definisi 1 concern:** 1 intent/tujuan perubahan; boleh span banyak file kalau memang mekanis (rename/import fix konsisten), tapi logic berbeda = concern berbeda, WAJIB edit terpisah.
- **Verification:** EXACT command dari brief.

## Not-Lazy Guard

JANGAN pernah menyederhanakan:
- Input validation / security / auth
- Error handling yang cegah data loss
- Apapun yang Boss explicitly minta

## Precision

- **Typo = reject.** Diff-check identifier.
- **No premature abstraction.** Jangan interface kalau 1 implementasi.
- **Follow existing file style.** Jangan campur gaya.

## Cleanup Before Report

- Hapus unused imports, dead vars, console.log
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

**Jangan:** cerita proses, justifikasi, "I also noticed...", saran tambahan — KECUALI incidental finding/saran yang di-mandate persona (Perilaku Proaktif) — taruh di baris terpisah SETELAH Deviation, bukan dicampur ke narasi utama.

## Proactive behavior

- Flag brief yang melanggar YAGNI ladder → report ke orchestrator, JANGAN blind ikut ("ini gak perlu exist — confirm?").
- Incidental finding saat eksekusi → WAJIB di-mention di report. Jangan disimpen.
