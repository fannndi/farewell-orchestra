---
name: verification-ground-truth
description: Use after implementation, before writing report — verify claims against actual tool output, never assume success. Complements minimal-impl.
---

> Cost Model: executor — write access, verify before report. Orchestrator never writes code.

# Verification & Ground-Truth

Boss nggak percaya kata "harusnya udah bener". Boss percaya output command. Setiap klaim "done" harus punya bukti eksekusi, bukan asumsi dari baca kode doang.

## Prinsip
Nggak pernah lapor "Done" sebelum diverifikasi via tool output. "Kode ini harusnya fix" ≠ "test pass". Yang pertama tebakan, yang kedua fakta.

## 1. Verify-Before-Claim

| Klaim | Cara verifikasi |
|-------|----------------|
| "Build passes" | Run build command, baca exit code |
| "Bug fixed" | Reproduce → fix → run ulang |
| "Test passes" | Run test suite, baca output |
| "File udah ke-update" | Baca ulang file setelah edit |

## 2. Assumption Firewall
- **Tool call sukses?** Cek return value. Jangan asumsi.
- **State masih sama?** Re-read sebelum edit kedua. Jangan asumsi.
- **Dependency ada?** Cek package.json/lockfile. Jangan asumsi.

## 3. Self-Check Sebelum Report

- [ ] Command verifikasi udah di-run barusan (bukan hasil run lama/basi)
- [ ] Output command itu beneran dibaca, bukan diasumsikan sukses karena "biasanya begitu"
- [ ] Kalau ada error di output — itu dilaporkan, bukan disembunyiin demi report keliatan clean
- [ ] Kalau verifikasi TIDAK BISA dijalanin (no test runner, no build script) — bilang terus terang kenapa, jangan klaim "should work"

## 4. Report Format (extend dari minimal-impl)

```
Done. X file(s) changed.
Verified: [command yang di-run] → [hasil aktual, bukan ekspektasi]
Unverified: [kalau ada bagian yang nggak bisa dicek — sebutkan kenapa]
```

**Jangan pernah** tulis "should work" atau "seharusnya fine" di report tanpa command yang mendukung. Kalau nggak sempat/nggak bisa verify — itu residual risk, bukan silent assumption.

## Mantra

> "Gue nggak lapor apa yang gue pikir bakal kejadian. Gue lapor apa yang gue liat kejadian."
