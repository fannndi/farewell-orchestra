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
**Contoh before/after:**
```
❌ BEFORE (45 baris, 4 class + helper):
class UserValidator:
    def __init__(self, config):
        self.config = config
    def validate_email(self, email):
        if not re.match(r'^[^@]+@[^@]+$', email):
            return False, "Invalid email"
        return True, ""
    def validate_password(self, password):
        if len(password) < 8:
            return False, "Password too short"
        return True, ""
    def validate_name(self, name):
        if not name.strip():
            return False, "Name empty"
        return True, ""
✅ AFTER (8 baris, 1 function):
def validate_user(email: str, password: str, name: str) -> tuple[bool, str]:
    if not re.match(r'^[^@]+@[^@]+$', email): return False, "Invalid email"
    if len(password) < 8: return False, "Password too short"
    if not name.strip(): return False, "Name empty"
    return True, ""
```
5. **Baru nulis kode.**
**Anti-patterns:**
- ❌ Bikin banyak file untuk fitur kecil
- ❌ Bikin abstraction untuk 1 implementasi
- ❌ Bikin pattern/dependency yang tidak perlu
- ❌ Observer pattern untuk 1 event
- ❌ Dependency baru yang tidak perlu
- ❌ Comment terlalu banyak
- ❌ Naming terlalu panjang
- ❌ Simple code > clever code
WAJIB sebelum nulis kode. Cek semua:
- [ ] **Goal jelas?** — Apa yang mau dicapai?
- [ ] **Scope kecil?** — Bisa 1 file? Bisa 10 baris?
- [ ] **Existing solution?** — Udah ada yang bisa dipakai?
- [ ] **Dependency perlu?** — Bisa tanpa dependency baru?
- [ ] **Pattern perlu?** — Bisa tanpa pattern?
| Kondisi | Keputusan |
|---------|-----------|
| < 100 baris | 1 file |
- **100-300 baris:** Split HANYA kalau ada 2+ tanggung jawab beda (contoh: validation + API call). Satu tanggung jawab → tetap 1 file.