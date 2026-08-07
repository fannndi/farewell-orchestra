---
name: error-handler
description: Error classification + recovery. Handle errors differently based on type.
activation: When error occurs
trigger: Sub-agent returns error
---

# Error Handler

Error classification + recovery. Handle errors differently based on type.

## Error Classification

| Type | Description | Recovery |
|------|-------------|----------|
| **RETRY** | Transient error, might work on retry | Retry dengan prompt lebih detail |
| **FALLBACK** | Error yang bisa di-handle dengan cara lain | Gunakan alternative approach |
| **ESCALATE** | Error yang butuh Boss intervention | Escalate ke Boss |
| **SKIP** | Error yang bisa di-skip | Skip, lanjut ke step berikut |
| **ABORT** | Error yang fatal, tidak bisa dilanjut | Stop, report ke Boss |

## Error Detection

| Error Pattern | Type | Recovery |
|---------------|------|----------|
| Timeout | RETRY (max 2) | Retry dengan prompt lebih pendek |
| Rate limit | RETRY (max 2) | Wait + retry |
| Format salah | RETRY | Retry dengan format reminder |
| File not found | FALLBACK | Cari file alternatif |
| Permission denied | ESCALATE | Butuh Boss intervention |
| Out of memory | ESCALATE | Butuh resource lebih |
| Invalid input | SKIP | Skip, report warning |
| Data corruption | ABORT | Stop, report ke Boss |

## Recovery Strategy

### RETRY Errors
```
1. Detect error type
2. Wait (kalau rate limit)
3. Retry dengan prompt lebih detail
4. Max 2 retries
5. Kalau masih gagal → ESCALATE
```

### FALLBACK Errors
```
1. Detect error type
2. Cari alternative approach
3. Gunakan alternative
4. Report: "Used alternative: [approach]"
```

### ESCALATE Errors
```
1. Detect error type
2. Report ke Boss: "Error: [type] — [description]"
3. Tunggu Boss response
4. Ikuti instruksi Boss
```

### SKIP Errors
```
1. Detect error type
2. Log warning
3. Skip step
4. Report: "Skipped: [reason]"
```

### ABORT Errors
```
1. Detect error type
2. Stop semua processing
3. Report ke Boss: "ABORT: [error] — [impact]"
4. Tunggu Boss instruksi
```

## Integration

- Orchestrator classify error setiap sub-agent response
- Sub-agents report error type di output
- Error handler suggest recovery strategy

## Contoh

**RETRY:**
```
[ERROR] Timeout researcher — retry 1/2
[ERROR] Timeout researcher — retry 2/2
[ESCALATE] Researcher timeout setelah 2 retries
```

**FALLBACK:**
```
[ERROR] File src/auth.ts tidak ditemukan
[FALLBACK] Menggunakan src/auth/index.ts sebagai alternatif
```

**ESCALATE:**
```
[ERROR] Permission denied ke production database
[ESCALATE] Butuh akses database dari Boss
```

## Cross-Project Error Handling

### Permission Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Permission denied" | Path not in whitelist | Add to opencode.jsonc external_directory |
| "Cannot access" | Invalid path | Verify path exists |
| "Access denied" | File locked | Wait and retry |

### Agent Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Agent timeout | Task too large | Reduce scope, re-chunk |
| Agent empty response | Model issue | Retry once, then escalate |
| Agent wrong format | Prompt unclear | Re-dispatch with format reminder |
| Agent crash | System issue | Report to Boss |

### File Errors

| Error | Cause | Fix |
|-------|-------|-----|
| File not found | Wrong path | Verify path, retry |
| File exists | Already created | Skip or overwrite |
| Directory not found | Missing parent | Create directory first |

### Recovery Strategy

1. **Permission errors** — fix config, retry
2. **Agent errors** — retry once, then escalate
3. **File errors** — fix path/permissions, retry
4. **System errors** — report to Boss, suggest restart

### Error Reporting Format

```
[ERROR] [type] — [description]
  Cause: [root cause]
  Fix: [solution]
  Status: [fixed/needs attention/escalated]
```
