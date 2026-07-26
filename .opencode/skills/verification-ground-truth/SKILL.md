---
name: verification-ground-truth
description: Use after implementation, before writing report — verify claims against actual tool output, never assume success. Complements `minimal-impl`.
---

# Verification & Ground-Truth

Boss nggak percaya kata "harusnya udah bener". Boss percaya output command. Setiap klaim "done" harus punya bukti eksekusi, bukan asumsi dari baca kode doang.

## Prinsip

**Nggak pernah lapor sesuatu yang belum lo verifikasi jalanin sendiri.** "Kode ini seharusnya fix bug-nya" ≠ "gue run test, hasilnya pass". Kalimat pertama itu tebakan bersampul percaya diri. Kalimat kedua itu fakta.

## 1. Verify-Before-Claim

Sebelum nulis "Done" di report, tanya ke diri sendiri:

| Klaim | Cara verifikasi wajib |
|-------|----------------------|
| "Build passes" | Run command build-nya, baca exit code + output — bukan nebak dari baca syntax |
| "Bug fixed" | Reproduce bug dulu (kalau bisa), lalu run ulang setelah fix, bandingin |
| "Test passes" | Run test suite/command spesifik, bukan cuma baca assertion di kode |
| "File udah ke-update" | Baca ulang file setelah edit — jangan asumsi `str_replace`/edit tool sukses |
| "Import valid" | Cek file target ada dan export yang dipakai emang ada di sana |

Kalau brief nggak kasih command verifikasi eksplisit → cari command yang paling relevan (package.json scripts, README, existing CI config) sebelum nanya Boss.

## 2. Assumption Firewall

- **Jangan asumsi tool call sukses.** Cek return value / error field, bukan cuma "kalau nggak ada exception berarti sukses".
- **Jangan asumsi state sebelumnya masih sama.** File yang lo baca di awal task bisa aja berubah kalau ada step lain di antaranya — re-read sebelum edit kedua kalinya kalau ada jeda tool call lain.
- **Jangan asumsi dependency ada.** Library yang dipanggil di kode — cek beneran ke-install (package.json/lockfile), bukan cuma "biasanya ada".
- **Ambigu antara dua kemungkinan?** → verifikasi keduanya lewat tool (baca file, run command) sebelum milih salah satu, jangan pilih yang "kelihatannya lebih mungkin".

## 3. Self-Check Sebelum Report

Checklist wajib sebelum kirim laporan ke orchestrator:

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
