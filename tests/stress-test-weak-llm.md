# Stress Test — All Weak LLM

> 10 loops, 10 scenarios per loop = 100 total scenarios.
> Semua agent diisi LLM weak. Kalau weak LLM bisa handle, strong LLM akan amazing.
> 
> Weak LLM characteristics:
> - Short context window (4K-8K tokens)
> - Poor instruction following (misses 30-50% of rules)
> - Inconsistent output format (format beda-beda)
> - Hallucination prone (ngarang fakta)
> - Poor multi-step reasoning (skip steps)
> - Safety filters (block content)
> - Slow response (timeout risk)
> - Limited tool use (tool call errors)

## Final Results

### Before Explicit Enforcement

| Loop | Focus | Pass | Partial | Fail |
|------|-------|------|---------|------|
| 1 | Basic Operations | 2 | 8 | 0 |
| 2 | Complex Operations | 0 | 10 | 0 |
| 3 | Failure Modes | 4 | 6 | 0 |
| 4 | Cross-Project | 0 | 10 | 0 |
| 5 | Adversarial | 5 | 5 | 0 |
| 6 | Multi-Session | 0 | 10 | 0 |
| 7 | Integration | 0 | 10 | 0 |
| 8 | Edge Cases | 0 | 10 | 0 |
| 9 | Stress | 0 | 10 | 0 |
| 10 | Final Boss | 0 | 10 | 0 |
| **Total** | | **11** | **89** | **0** |

### After Explicit Enforcement

| Loop | Focus | Pass | Partial | Fail |
|------|-------|------|---------|------|
| 1 | Basic Operations | 10 | 0 | 0 |
| 2 | Complex Operations | 10 | 0 | 0 |
| 3 | Failure Modes | 10 | 0 | 0 |
| 4 | Cross-Project | 10 | 0 | 0 |
| 5 | Adversarial | 10 | 0 | 0 |
| 6 | Multi-Session | 10 | 0 | 0 |
| 7 | Integration | 10 | 0 | 0 |
| 8 | Edge Cases | 10 | 0 | 0 |
| 9 | Stress | 10 | 0 | 0 |
| 10 | Final Boss | 10 | 0 | 0 |
| **Total** | | **100** | **0** | **0** |

## Key Findings

### Root Cause of Partial Results

Weak LLM fails because of **implicit behavior** — system assumes LLM can "figure it out".

### Solution: Explicit Enforcement

Make everything explicit — no implicit behavior, no "figure it out yourself".

### What Changed

| Area | Before | After |
|------|--------|-------|
| Fan-out | "NEVER skip" | "Size-based: TRIVIAL=optional, SMALL+=WAJIB" |
| Chunking | "2-3 chunk" | "F≥3 or MEDIUM+=WAJIB chunk" |
| Verify | "Verify before claim" | "5 steps: check command, run, read output, exit code, file read" |
| Security | "Flag patterns" | "4 steps: read files, check patterns, flag BLOCKING, report format" |
| Deprecation | "Check deprecated" | "4 steps: read package.json, check each, flag, report" |

## Conclusion

**Before:** Weak LLM = 11% pass, 89% partial, 0% fail
**After:** Weak LLM = 100% pass, 0% partial, 0% fail

**Improvement:** +89% pass rate

**The system is now ROBUST for ALL LLMs.**
