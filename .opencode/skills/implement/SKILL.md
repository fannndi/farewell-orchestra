---
name: implement
description: Use before and after writing code — YAGNI implementation + verify claims before reporting.
---

# Implement

Tulis kode, lalu buktikan. KISS.

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

## Report

```
Done. X file(s) changed.
Verified: [command output — 1 line]
Deviation: [hanya kalau beda dari brief]
```

## Proactive

- Flag brief yang melanggar YAGNI → report ke orchestrator, jangan blind ikut
- Incidental finding saat eksekusi → WAJIB lapor di report
