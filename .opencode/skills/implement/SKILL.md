---
name: implement
description: Tulis kode KISS, verify, selesai.
activation: When dispatched by orchestrator
trigger: Orchestrator dispatches executor
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

## Cross-Project Implementation

### Project Type Detection
Before implementing, detect project type:
```
pubspec.yaml     → Flutter/Dart
package.json     → Node.js
requirements.txt → Python
Cargo.toml       → Rust
go.mod           → Go
```

### Project-Specific Commands

| Type | Test | Build | Lint |
|------|------|-------|------|
| Flutter | `flutter test` | `flutter build apk` | `flutter analyze` |
| Node.js | `npm test` | `npm run build` | `npm run lint` |
| Python | `pytest` | `python -m build` | `ruff check .` |
| Rust | `cargo test` | `cargo build` | `cargo clippy` |
| Go | `go test ./...` | `go build ./...` | `golangci-lint run` |

### Permission Handling
If executor kena permission block:
1. Report: "Permission denied untuk path X"
2. Orchestrator akan update config
3. Retry after config update

### File Creation Pattern
When creating files in external project:
1. Use absolute paths
2. Create directories if needed
3. Verify file exists after creation
4. Report: "File created: [path]"

## Implementation Checklist

- [ ] Brief dipahami (TASK, FILES, CONTEXT, VERIFY)
- [ ] Project type detected
- [ ] Existing code dibaca (jangan overwrite yang sudah ada)
- [ ] Kode ditulis sesuai KISS
- [ ] Verify command dijalankan
- [ ] Hasil dilaporkan

## Error Recovery

### Build Fails
1. Read error message
2. Fix syntax/import issues
3. Retry build
4. If still fails → report error ke orchestrator

### Test Fails
1. Read test output
2. Fix implementation
3. Retry test
4. If still fails → report ke orchestrator

### Permission Denied
1. Report: "Permission denied: [path]"
2. Don't retry — orchestrator will fix config
