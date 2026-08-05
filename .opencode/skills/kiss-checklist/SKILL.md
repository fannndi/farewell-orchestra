---
name: kiss-checklist
description: Pre-implementation checklist. WAJIB sebelum nulis kode.
---

# KISS Checklist

WAJIB sebelum nulis kode. Cek semua.

## Pre-Implementation

- [ ] **Goal jelas?** — Apa yang mau dicapai?
- [ ] **Scope kecil?** — Bisa 1 file? Bisa 10 baris?
- [ ] **Existing solution?** — Udah ada yang bisa dipakai?
- [ ] **Dependency perlu?** — Bisa tanpa dependency baru?
- [ ] **Pattern perlu?** — Bisa tanpa pattern?

## Decision: Pisah File?

| Kondisi | Keputusan |
|---------|-----------|
| < 100 baris | 1 file |
| 100-300 baris | Pertimbangkan pisah kalau domain beda |
| > 300 baris | Pisahkan dengan alasan jelas |
| Logic beda | Pisahkan (misal: auth vs utils) |
| Logic sama | Jangan pisahkan |

## Decision: Bikin Abstraction?

| Kondisi | Keputusan |
|---------|-----------|
| Dipakai 1x | Langsung, jangan abstraksi |
| Dipakai 2x | Pertimbangkan, tapi boleh langsung |
| Dipakai 3x+ | Buat abstraction |
| Complexity tinggi | Hindari abstraction |

## Decision: Tambah Dependency?

| Kondisi | Keputusan |
|---------|-----------|
| Stdlib bisa | Pakai stdlib |
| 10 baris bisa | Tulis sendiri |
| Complex + dipakai banyak | Tambah dependency |
| Simple + dipakai sedikit | Tulis sendiri |

## Anti-Patterns (JANGAN)

- ❌ 7 file untuk fitur kecil
- ❌ Abstract class untuk 1 implementasi
- ❌ Factory pattern untuk 1 objek
- ❌ Strategy pattern untuk 1 strategi
- ❌ Observer pattern untuk 1 event
- ❌ Dependency baru yang tidak perlu
- ❌ Comment terlalu banyak
- ❌ Naming terlalu panjang

## Post-Implementation

- [ ] **Kode works?** — Verify command pass
- [ ] **Kode simple?** — Bisa lebih sederhana?
- [ ] **Kode clean?** — Unused code dihapus?
- [ ] **Kode minimal?** — Tidak ada yang mubazir?
