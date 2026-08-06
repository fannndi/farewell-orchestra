# Skills: executor

=== implement ===
---
name: implement
description: Tulis kode KISS, verify, selesai.
activation: When dispatched by orchestrator
trigger: Orchestrator dispatches executor
---
Tulis kode yang **simple, modular, efisien**. KISS.
Sebelum nulis kode, tanya:
1. **Perlu exist?** → Tidak? Stop. Hapus.
**Jangan hapus kalau:** dipakai module lain, punya test, di jalur aktif. **Hapus kalau:** confirmed dead code (0 caller), tidak ada test, tidak ada import chain.
2. **Stdlib bisa?** → Pakai stdlib.
3. **1 file cukup?** → Jangan pisah.
4. **10 baris cukup?** → Jangan bikin 100.