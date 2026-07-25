---
name: scope-guard
description: Use pre-execution to verify scope boundaries. Warns if proposed changes touch files outside declared scope. Always invoked during guardrail scan.
---

## Purpose

Prevent scope creep. Before any executor dispatch, verify that all files to be modified are within the declared scope. If a change touches files outside scope, flag it as WARNING — Boss must explicitly approve before execution.

## Trigger

Invoke AUTOMATICALLY during orchestrator pre-flight guardrail scan:
- Before every executor dispatch
- When orchestrator is about to delegate implementation
- After assumption logger completes

## Process

1. **Read declared scope** from brief template (explicit file/folder list)
2. **Trace impact** — if modifying function X, what files import/use X? Grep references.
3. **Compare** — any impacted file outside declared scope?
4. **Verdict** — CLEAN (all in scope) or WARN (some out of scope)
5. **If WARN** — list out-of-scope files. Boss decides: expand scope or constrain change.

## Output Format

**CLEAN:**
```
🔬 Scope: bersih. Semua perubahan dalam [scope].
```

**WARN:**
```
⚠️ Scope Warning:
   Dalam scope: [file A, file B]
   Di luar scope: [file X — import fungsi Y, file Z — test akan break]
   
   Lanjut dengan scope diperluas? Atau constrain ke [scope] aja?
```

## Rules

- Silent kalau CLEAN. Hanya report kalau WARN.
- Test files TERMASUK dalam scope check. Kalau kode berubah, test harus diupdate → itu bagian dari scope.
- Config files (.env, opencode.jsonc, package.json) — WARN kalau berubah tanpa eksplisit disebut.
- Grep selalu pakai exact symbol name. Jangan substring match longgar.
- Max 5 out-of-scope files dilaporkan. Lebih dari itu → "⚠️ Terlalu banyak file di luar scope. Perlu redefine scope."

## Failure Modes

- **False positive** — flag file yang sebenarnya related (test file, type definition). Gunakan common sense.
- **False negative** — tidak flag file yang jelas kena impact. Selalu grep references.
- **Noise** — melaporkan 20 file di luar scope. Batasi ke 5 paling critical.
```
