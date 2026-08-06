---
name: complexity-budget
description: Limit complexity per feature. Kalau melebihi, pecah atau sederhanakan.
activation: When checking limits
trigger: Reviewer checks budget
---

# Complexity Budget

Limit complexity per feature. Kalau melebihi, pecah atau sederhanakan.

## Budget Per Feature

| Metric | Budget | Action kalau melebihi |
|--------|--------|----------------------|
| Files | ≤ 3 | Gabung atau pecah jadi sub-feature |
| Lines | ≤ 300 | Sederhanakan atau pecah |
| Functions | ≤ 10 | Gabung atau pecah |
| Dependencies | ≤ 5 | Hapus yang tidak perlu |
| Abstraction layers | ≤ 2 | Hapus abstraction |

## Budget Per File

| Metric | Budget | Action kalau melebihi |
|--------|--------|----------------------|
| Lines | ≤ 300 | Pecah jadi 2 file |
| Functions | ≤ 10 | Pecah jadi 2 file |
| Parameters | ≤ 5 | Gunakan object |
| Nesting depth | ≤ 3 | Extract function |

## Budget Per Function

| Metric | Budget | Action kalau melebihi |
|--------|--------|----------------------|
| Lines | ≤ 30 | Pecah jadi 2 function |
| Parameters | ≤ 5 | Gunakan object |
| Nesting depth | ≤ 3 | Extract function |
| Cyclomatic complexity | ≤ 10 | Sederhanakan logic |

## Contoh: Budget Check

### Feature: User Authentication

```
Files: 1 ✅ (budget: ≤3)
Lines: 150 ✅ (budget: ≤300)
Functions: 5 ✅ (budget: ≤10)
Dependencies: 2 ✅ (budget: ≤5)
Abstraction layers: 1 ✅ (budget: ≤2)
```

**Result:** PASS — dalam budget

### Feature: E-commerce Checkout

```
Files: 8 ❌ (budget: ≤3)
Lines: 1200 ❌ (budget: ≤300)
Functions: 45 ❌ (budget: ≤10)
Dependencies: 12 ❌ (budget: ≤5)
Abstraction layers: 4 ❌ (budget: ≤2)
```

**Result:** FAIL — melebihi budget

**Action:** Pecah jadi sub-features:
1. Cart (2 file, 200 baris)
2. Payment (2 file, 250 baris)
3. Confirmation (1 file, 100 baris)
4. Email (1 file, 50 baris)

## Enforcement

**Executor:** Cek budget sebelum report
**Reviewer:** Flag kalau melebihi budget
**Orchestrator:** Pecah task kalau melebihi budget

## Contoh: Enforcement

### Scenario: Feature melebihi budget

```
[SHOULD] src/checkout.ts — 450 lines (budget: 300) — pecah jadi 2 file
[SHOULD] src/checkout.ts — 15 functions (budget: 10) — pecah jadi 2 file
```

### Scenario: Feature dalam budget

```
[PASS] src/auth.ts — 150 lines (budget: 300)
[PASS] src/auth.ts — 5 functions (budget: 10)
```
