---
name: kiss-automation
description: Automated KISS checks using tools.
activation: Before reporting done
trigger: Executor selesai implement
---

# KISS Automation

Automated checks untuk memastikan kode KISS.

## Checks

### 1. File Count Check
```bash
# Cek berapa file per feature
find . -name "*.py" -o -name "*.ts" -o -name "*.js" | wc -l
```
**Target:** ≤3 files per feature

### 2. Line Count Check
```bash
# Cek berapa baris per file
wc -l src/*.py src/*.ts
```
**Target:** ≤300 lines per file

### 3. Complexity Check (Python)
```bash
# Gunakan ruff untuk cek complexity
ruff check --select C901 src/
```
**Target:** Cyclomatic complexity ≤10

### 4. Dead Code Check (Python)
```bash
# Gunakan vulture untuk cek dead code
vulture src/ --min-confidence 80
```
**Target:** 0 dead code

### 5. Duplication Check
```bash
# Gunakan jscpd untuk cek duplikasi
jscpd src/ --min-lines 5 --min-tokens 50
```
**Target:** <5% duplication

### 6. Magic Numbers Check
```bash
# Gunakan ruff untuk cek magic numbers
ruff check --select PLR2004 src/
```
**Target:** 0 magic numbers

### 7. Naming Check
```bash
# Gunakan ruff untuk cek naming
ruff check --select N src/
```
**Target:** Semua nama konsisten

## Automation Flow

```
Executor selesai
  │
  ▼
Run kiss-automation checks
  │
  ├── PASS → report "KISS verified"
  └── FAIL → report issues, fix before report
```

## Rules

1. **Run semua checks** sebelum report "Done"
2. **Kalau ada FAIL** → fix dulu
3. **Kalau semua PASS** → report "KISS verified"
4. **Jangan skip** — ini quality gate

## Output

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
