---
name: prepare
description: Validate input before dispatch.
---

# Prepare

Validate input, extract requirements.

## Steps

1. Cek: goal jelas? Scope jelas?
   - Jelas → PASS
   - Tidak → HOLD, tanya Boss
2. Kalau PASS → tentukan size (TRIVIAL/SMALL/MEDIUM/LARGE)
3. Chunk kalau perlu

## Output

- `PASS [SIZE]` → lanjut ke orchestrate
- `HOLD [alasan]` → tanya Boss
