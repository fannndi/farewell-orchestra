---
name: implement
description: Tulis kode KISS, verify, selesai.
activation: When dispatched by orchestrator
trigger: Orchestrator dispatches executor
---

# Implement

Tulis kode yang **simple, modular, efisien**. KISS.

## KISS Rules

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

## Pre-Implementation Checklist

WAJIB sebelum nulis kode. Cek semua:

- [ ] **Goal jelas?** — Apa yang mau dicapai?
- [ ] **Scope kecil?** — Bisa 1 file? Bisa 10 baris?
- [ ] **Existing solution?** — Udah ada yang bisa dipakai?
- [ ] **Dependency perlu?** — Bisa tanpa dependency baru?
- [ ] **Pattern perlu?** — Bisa tanpa pattern?

### Decision: Pisah File?

| Kondisi | Keputusan |
|---------|-----------|
| < 100 baris | 1 file |
- **100-300 baris:** Split HANYA kalau ada 2+ tanggung jawab beda (contoh: validation + API call). Satu tanggung jawab → tetap 1 file.
| > 300 baris | Pisahkan dengan alasan jelas |
| Logic beda | Pisahkan (misal: auth vs utils) |
| Logic sama | Jangan pisahkan |

### Decision: Bikin Abstraction?

| Kondisi | Keputusan |
|---------|-----------|
| Dipakai 1x | Langsung, jangan abstraksi |
- **Dipakai 2x:** Inline, KECUALI code >10 baris DAN identik di 2 tempat → extract function.
| Dipakai 3x+ | Buat abstraction |
| Complexity tinggi | Hindari abstraction |

**Complexity tinggi =** file >200 baris OR function >50 baris OR nesting >3 OR cyclomatic >10 OR imports >8 modules (sinkron dengan ../../agents/reviewer.md).

### Decision: Tambah Dependency?

| Kondisi | Keputusan |
|---------|-----------|
| Stdlib bisa | Pakai stdlib |
| 10 baris bisa | Tulis sendiri |
| Complex + dipakai banyak | Tambah dependency |
| Simple + dipakai sedikit | Tulis sendiri |

## Verify

Setiap klaim "done" harus punya bukti:

| Klaim | Verifikasi |
|-------|-----------|
| "Build passes" | Run build command |
| "Test passes" | Run test command |
| "File updated" | Baca ulang file |

**Sumber VERIFY command:** dari brief (field VERIFY). Kalau brief tidak ada → pakai default project (Node: `npm test`; Python: `pytest`; Flutter: `flutter test`; Rust: `cargo test`). Tidak ada default → report "No verify command. Manual check required."

## Implementation Checklist

- [ ] Brief dipahami (TASK, FILES, CONTEXT, VERIFY)
- [ ] Existing code dibaca (jangan overwrite)
- [ ] Verify command dijalankan & hasil dilaporkan

## Post-Implementation Checklist

- [ ] **Kode works?** — Verify command pass
- [ ] **Kode simple?** — Bisa lebih sederhana?
- [ ] **Kode clean?** — Unused code dihapus?
- [ ] **Kode minimal?** — Tidak ada yang mubazir?

## Automated KISS Checks

Jalankan sebelum report "Done". Semua PASS → report "KISS verified". Ada FAIL → fix dulu.

| # | Check | Command | Target |
|---|-------|---------|--------|
| 1 | File count per feature | `find . -name "*.py" -o -name "*.ts" -o -name "*.js" \| wc -l` | ≤3 files |
| 2 | Line count per file | `wc -l src/*.py src/*.ts` | ≤300 lines |
| 3 | Complexity (Python) | `ruff check --select C901 src/` | ≤10 cyclomatic |
| 4 | Dead code (Python) | `vulture src/ --min-confidence 80` | 0 dead code |
| 5 | Duplication | `jscpd src/ --min-lines 5 --min-tokens 50` | <5% duplication |
| 6 | Magic numbers | `ruff check --select PLR2004 src/` | 0 magic numbers |
| 7 | Naming | `ruff check --select N src/` | Nama konsisten |

**Cross-platform:** Linux/Mac pakai `find`/`wc -l`. Windows PowerShell: file count `(Get-ChildItem -Recurse -Include *.py,*.ts,*.js).Count`, line count `(Get-Content src/*.py | Measure-Object -Line).Lines`. Kalau tool/command tidak ada → skip + note "Tool [X] not available, skipped."

### Automation Flow

```
Executor selesai
  │
  ▼
Run KISS checks
  ├── PASS → report "KISS verified"
  └── FAIL → fix dulu, baru report
```

**Fix loop max:** 2 iterasi. Masih gagal → report hasil + note "[FAIL after 2 fix attempts, needs orchestrator review]".

### Output

```
KISS Automation Results:
✅ File count: 2 files (target: ≤3)
✅ Line count: 150 lines (target: ≤300)
✅ Complexity: 5 (target: ≤10)
✅ Dead code: 0
✅ Duplication: 2% (target: <5%)
✅ Magic numbers: 0
✅ Naming: consistent

KISS verified.
```

## Output

```
Done. X file(s) changed.
Verified: <command output — 1 line: pass/fail + key metric>
KISS: <PASS/FAIL> — <detail kalau FAIL>
```

Contoh: `Done. 2 files changed. Verified: 47 tests passed (0 failures, 12.3s). KISS: PASS — 2 files, 45 lines.`

## Cross-Project

See AGENTS.md Cross-Project Handling.

## Error Recovery

See AGENTS.md Error Recovery.
