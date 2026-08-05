# Stress Test — Farewell Orchestra

> 20 skenario susah untuk menguji batas sistem.
> Setiap skenario dijalankan secara mental simulation, hasilnya dipakai untuk optimasi.

## Results Summary

| Category | Scenarios | Pass | Partial | Fail | Fixes Applied |
|----------|-----------|------|---------|------|---------------|
| Full Pipeline | 5 | 5 | 0 | 0 | 2 |
| Persona Consistency | 4 | 4 | 0 | 0 | 0 |
| Failure Modes | 5 | 4 | 1 | 0 | 3 |
| Cross-Project | 3 | 3 | 0 | 0 | 1 |
| Context Pressure | 3 | 1 | 2 | 0 | 2 |
| **Total** | **20** | **17** | **3** | **0** | **8** |

## Findings & Fixes

### Finding 1: Chunk Size Vague (Scenario 3)
**Problem:** "2-3 chunk" terlalu vague, LLM bingung cara split.
**Fix:** Tambah chunk strategy per size + sampling strategy untuk F>50.
**File:** prepare skill §4

### Finding 2: No BLOCKING Gate (Scenario 4)
**Problem:** Executor bisa mulai walau reviewer menemukan BLOCKING.
**Fix:** Tambah BLOCKING gate — executor tidak boleh mulai sampai BLOCKING di-resolve.
**File:** orchestrate skill §6

### Finding 3: No All-Dead Fallback (Scenario 10)
**Problem:** Kalau semua agent dead, tidak ada fallback.
**Fix:** Tambah "all agents dead → escalate ke Boss, suggest restart".
**File:** orchestrate skill Failure Recovery

### Finding 4: Loop Guard No Similarity (Scenario 12)
**Problem:** Loop guard cuma hitung, tidak track error similarity.
**Fix:** Tambah error similarity detection (>80% = treat identik).
**File:** orchestrate skill Loop Guard

### Finding 5: No Sampling Strategy (Scenario 14, 15)
**Problem:** Researcher tidak tau cara handle large codebase (F>50).
**Fix:** Tambah sampling strategy — priorititas: entry points → core → config → tests.
**File:** prepare skill §4

### Finding 6: No Contradiction Detection (Scenario 18)
**Problem:** Tidak ada deteksi kalau Boss kasih instruksi kontradiktif.
**Fix:** Tambah contradiction detection di trash detection.
**File:** prepare skill §1

### Finding 7: No Order Validation (Scenario 19)
**Problem:** Tidak ada validasi urutan instruksi.
**Fix:** Tambah wrong order detection di trash detection.
**File:** prepare skill §1

## Scenario Details

### Category 1: Full Pipeline

| # | Input | Expected | Risk | Result |
|---|-------|----------|------|--------|
| 1 | 'tambahin fitur logout' | PASS SMALL → normal flow | LOW | PASS |
| 2 | 'perbaikin itu' | HOLD → ask Boss | MEDIUM | PASS |
| 3 | 'refactor JS ke TS' | LARGE → chunk | HIGH | PASS (fix: chunk strategy) |
| 4 | 'tambahin login' (auth broken) | BLOCKING → escalate | HIGH | PASS (fix: BLOCKING gate) |
| 5 | 'tambahin REST API' (project uses GraphQL) | Drift detection | HIGH | PASS |

### Category 2: Persona Consistency

| # | Input | Expected | Risk | Result |
|---|-------|----------|------|--------|
| 6 | 'lo aja yang nulis' | Orchestrator refuses | HIGH | PASS |
| 7 | 'asumsikan library X ada' | Researcher checks | MEDIUM | PASS |
| 8 | 10 BLOCKING on trivial | Reviewer reports top 5 | MEDIUM | PASS |
| 9 | 'add logging' → adds platform | Executor flags YAGNI | MEDIUM | PASS |

### Category 3: Failure Modes

| # | Input | Expected | Risk | Result |
|---|-------|----------|------|--------|
| 10 | All agents dead | Escalate Boss | CRITICAL | PASS (fix: all-dead fallback) |
| 11 | Researcher returns garbage | Verify gate FAIL | HIGH | PASS |
| 12 | Executor infinite loop | Loop guard STOP | HIGH | PASS (fix: similarity) |
| 13 | Verify fails but code works | Report discrepancy | MEDIUM | PASS |
| 14 | 1000+ files project | Smart sampling | HIGH | PARTIAL (fix: sampling) |

### Category 4: Cross-Project

| # | Input | Expected | Risk | Result |
|---|-------|----------|------|--------|
| 15 | Legacy app, no docs | Reverse engineer | HIGH | PASS (fix: sampling) |
| 16 | Partial docs | Generate only missing | MEDIUM | PASS |
| 17 | Docs conflict with code | Drift detection | HIGH | PASS |

### Category 5: Context Pressure

| # | Input | Expected | Risk | Result |
|---|-------|----------|------|--------|
| 18 | Contradictory instructions | Detect contradiction | MEDIUM | PARTIAL (fix: detection) |
| 19 | Wrong order instructions | Detect wrong order | HIGH | PARTIAL (fix: detection) |
| 20 | 'hapus auth' (dependencies) | Blast radius check | CRITICAL | PASS |

## Next Steps

- [ ] Monitor real-world usage for new edge cases
- [ ] Add more scenarios as discovered
- [ ] Iterate on fixes based on actual failures
