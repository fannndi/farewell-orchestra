---
name: edge-cases
description: Handle edge cases in codebase analysis.
activation: When investigating codebase
trigger: Researcher starts investigation
---

# Edge Cases

Handle edge cases saat investigasi codebase.

## Edge Cases

### 1. Empty Project
**Detection:** Tidak ada file source code
**Action:** 
- Report: "Project kosong. Tidak ada kode."
- Suggest: "Mau scaffold project baru?"

### 2. Huge Project (>1000 files)
**Detection:** Banyak file
**Action:**
- Sampling: Prioritaskan entry points → core → config
- Max 50 files per investigation
- Report: "Project besar. Sample 50 file terpenting."

### 3. Binary Files
**Detection:** File .png, .jpg, .pdf, .exe, dll
**Action:**
- Skip binary files
- Report: "Skip N binary files"

### 4. Unicode/Emoji
**Detection:** Karakter non-ASCII di code
**Action:**
- Flag: "Unicode detected di [file:line]"
- Tidak BLOCKING, tapi catat

### 5. Symlinks
**Detection:** File yang merupakan symlink
**Action:**
- Follow symlink, tapi flag
- Report: "Symlink detected: [file] → [target]"

### 6. Hidden Files (.env, .git)
**Detection:** File yang diawali titik
**Action:**
- .env → SKIP (sensitive)
- .git → SKIP (git internal)
- .config → READ (config penting)

### 7. Very Long File Names (>200 chars)
**Detection:** Nama file panjang
**Action:**
- Flag: "File name terlalu panjang: [file]"
- Tidak BLOCKING, tapi catat

### 8. Special Characters in Paths
**Detection:** Spasi, karakter khusus di path
**Action:**
- Quote path dengan benar
- Flag kalau ada masalah

### 9. Circular Dependencies
**Detection:** A → B → C → A
**Action:**
- Report: "Circular dependency: A → B → C → A"
- BLOCKING kalau melibatkan core modules

### 10. Race Conditions
**Detection:** Concurrent access ke shared resource
**Action:**
- Report: "Potential race condition di [file:line]"
- BLOCKING kalau melibatkan data mutation

## Detection Rules

1. **Cek file types** — skip binary, .git, .env
2. **Cek file count** — sampling kalau >1000
3. **Cek dependencies** — detect circular
4. **Cek concurrency** — detect race conditions
5. **Report semua** — jangan simpan edge cases

## Output

```
Edge Cases Detected:
- Binary files: 5 (skipped)
- Hidden files: 3 (.env skipped, .config read)
- Unicode: 2 files
- Symlinks: 1
- Circular deps: 0
- Race conditions: 0
```
