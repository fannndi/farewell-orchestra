---
name: implement
description: Tulis kode KISS, verify, selesai.
---

# Implement

Tulis kode yang **simple, modular, efisien**. KISS.

## YAGNI Ladder

Sebelum nulis kode, tanya:

1. **Perlu exist?** → Tidak? Stop. Hapus.
2. **Stdlib bisa?** → Pakai stdlib.
3. **1 file cukup?** → Jangan pisah.
4. **10 baris cukup?** → Jangan bikin 100.
5. **Baru nulis kode.**

## Rules

1. **KISS** — kode paling sederhana yang works
2. **YAGNI** — kalau ragu perlu, jawabnya TIDAK
3. **1 file kalau bisa** — jangan pisahkan kalau tidak perlu
4. **1 fungsi kalau bisa** — jangan bikin banyak kalau cukup 1
5. **Verify** — tidak ada "done" tanpa bukti

## Anti-Over-Engineering

**Jangan:**
- ❌ Bikin banyak file untuk fitur kecil
- ❌ Bikin abstraction untuk 1 implementasi
- ❌ Bikin pattern yang tidak perlu
- ❌ Tambah dependency yang tidak perlu

**Lakukan:**
- ✅ Tulis langsung, refactor kalau perlu
- ✅ Simple code > clever code
- ✅ Hapus yang nggak dipakai

## Verify

Setiap klaim "done" harus punya bukti:

| Klaim | Verifikasi |
|-------|-----------|
| "Build passes" | Run build command |
| "Test passes" | Run test command |
| "File updated" | Baca ulang file |

## Output Format

```
Done. <X> file(s) changed.
Verified: <command output — 1 line>
```
