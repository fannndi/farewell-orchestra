# Skills: executor

=== implement ===
---
name: implement
description: Tulis kode KISS, verify, selesai.
---
Tulis kode yang **simple, modular, efisien**. KISS.
Sebelum nulis kode, tanya:
1. **Perlu exist?** → Tidak? Stop. Hapus.
2. **Stdlib bisa?** → Pakai stdlib.
3. **1 file cukup?** → Jangan pisah.
4. **10 baris cukup?** → Jangan bikin 100.
5. **Baru nulis kode.**

=== kiss-checklist ===
---
name: kiss-checklist
description: Pre-implementation checklist. WAJIB sebelum nulis kode.
---
WAJIB sebelum nulis kode. Cek semua.
- [ ] **Goal jelas?** — Apa yang mau dicapai?
- [ ] **Scope kecil?** — Bisa 1 file? Bisa 10 baris?
- [ ] **Existing solution?** — Udah ada yang bisa dipakai?
- [ ] **Dependency perlu?** — Bisa tanpa dependency baru?
- [ ] **Pattern perlu?** — Bisa tanpa pattern?
| Kondisi | Keputusan |

=== simplification ===
---
name: simplification
description: Guide untuk menyederhanakan kode yang sudah ada.
---
Cara menyederhanakan kode yang sudah ada.
> "Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away." — Antoine de Saint-Exupéry
Tanya:
- Ada file yang tidak perlu?
- Ada abstraction yang tidak perlu?
- Ada pattern yang tidak perlu?
- Ada dependency yang tidak perlu?