---
name: implement
description: Use before and after writing code — YAGNI implementation + verify claims before reporting.
---

# Implement

Tulis kode, lalu buktikan. KISS.

## Simplified Mode (untuk LLM lemah)

Kalau LLM tidak bisa handle complex instructions:

1. **Baca** — baca brief dari orchestrator
2. **Tulis** — tulis kode sesuai brief
3. **Verify** — jalankan verify command
4. **Lapor** — format: `Done. <X> file(s) changed. Verified: <output>.`

Contoh: `Done. 1 file changed. Verified: pytest pass.`

Jangan pakai quality gates kalau bingung. Cukup verify command.

## YAGNI Ladder

1. **Does this need to exist?** → No? Stop. Delete.
2. **Stdlib does it?** → Use it.
3. **Platform covers it?** → CSS over JS. DB constraint over app code.
4. **Existing dep solves it?** → Use it. NEVER add new dep.
5. **One line?** → One line.
6. **Only then:** minimum code that works.

## Rules

- Satu change per edit. Definisi 1 concern: 1 intent perubahan.
- Prefer delete over add. Hapus 5 > tambah 3.
- Follow existing file style. Jangan campur gaya.
- Typo = reject. Diff-check identifier.
- No premature abstraction. Jangan interface kalau 1 implementasi.

## Not-Lazy Guard

JANGAN sederhanakan: input validation, security, auth, error handling yang cegah data loss, apapun yang Boss explicitly minta.

## Error Healing

| Error | Action |
|-------|--------|
| Typo/import/syntax | Fix langsung |
| Timeout/rate limit | 1x retry: kurangi max_tokens 30% |
| Tool call malformed | 1x retry dengan argumen berbeda |
| Tool not found/permission denied | STOP. Eskalasi. |
| Logic error | 1x retry dengan asumsi berbeda |
| Structural error | STOP. Eskalasi. |

## Assumption Firewall

- **Tool call sukses?** Cek return value. Jangan asumsi.
- **State masih sama?** Re-read sebelum edit kedua. Jangan asumsi.
- **Dependency ada?** Cek package.json/lockfile. Jangan asumsi.

## Quality Gates — WAJIB sebelum report "Done"

```markdown
## Quality Check

- [ ] Verify command dijalankan dan exit code = 0
- [ ] Output verify dibaca (bukan diasumsikan sukses)
- [ ] File yang diedit dibaca ulang setelah edit
- [ ] Diff sesuai scope (no extra files)
- [ ] Naming konsisten dengan existing code
- [ ] No unused imports/dead vars/console.log
- [ ] No TODO/FIXME introduced
```

**Semua checklist WAJIB [x] sebelum report "Done".** Kalau ada yang belum → lanjut dulu.

## Verify Before Claim

Setiap klaim "done" harus punya bukti eksekusi:

| Klaim | Verifikasi |
|-------|-----------|
| "Build passes" | Run build command, baca exit code |
| "Bug fixed" | Reproduce → fix → run ulang |
| "Test passes" | Run test suite, baca output |
| "File updated" | Baca ulang file setelah edit |

**Jangan pernah** tulis "should work" tanpa command yang mendukung.

**Verify discrepancy:** Kalau verify command gagal tapi kode terlihat works → report: "Verify failed: [error]. Manual inspection: [observation]. Discrepancy perlu investigasi." Jangan dismiss error.

## DoD — Definition of Done

- Verification passes (per brief)
- Zero broken references
- No TODO/FIXME introduced
- Diff matches scope — no extra files
- Naming consistent
- Lint clean

## Cleanup

- Hapus unused imports, dead vars, console.log
- Cek naming consistency

## Report Format

```
Done. X file(s) changed.
Verified: [command output — 1 line]
Quality: [x/x gates passed]
Deviation: [hanya kalau beda dari brief]
```

**Contoh bagus:**
```
Done. 1 file changed.
Verified: pytest pass (3 tests, 0 failures)
Quality: 7/7 gates passed
```

**Contoh buruk:**
```
I've completed the implementation. I made changes to the authentication module.
The changes should fix the login issue. I also noticed some other things that
could be improved. Let me know if you need anything else.
```

## Proactive

- Flag brief yang melanggar YAGNI → report ke orchestrator, jangan blind ikut
- Incidental finding saat eksekusi → WAJIB lapor di report
