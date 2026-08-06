---
name: error-handler
description: Error classification + recovery. Handle errors differently based on type.
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
| Timeout | RETRY | Retry dengan prompt lebih pendek |
| Rate limit | RETRY | Wait + retry |
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
