---
name: orchestrate
description: Decompose request, fan-out parallel, synthesize results, delegate to executor
---

# Orchestrate

Satu-satunya koordinator. Input sudah CLEAN dari anti-gigo. Sekarang dekomposisi dan delegasi.

## 1. Decompose

- Pecah request jadi **work packages independen**
- Tiap package: bisa dikerjakan tanpa menunggu hasil package lain
- Tidak boleh ada overlap antar package
- Tiap package muat dalam **5 baris brief**

## 2. Fan-Out

Dispatch parallel untuk tiap work package:

| Task type | Agent | Read-only? |
|-----------|-------|------------|
| Code investigation | researcher | ✅ |
| Architecture/security audit | reviewer | ✅ |
| Implementation | executor (tunggu sintesis) | ❌ |

Researcher + reviewer **selalu parallel** kalau keduanya dibutuhkan.

## 3. Synthesize

Setelah researcher + reviewer selesai:
- Gabungkan findings → **max 3 bullet points**
- Conflict? → prioritaskan reviewer (keamanan > kenyamanan)
- Siapkan executor brief dari hasil sintesis

## 4. Delegate

Executor brief format:
```
Task: [1 kalimat]
Files: [path, path]
Constraints: [1-2 batasan]
Verify: [command]
```

**Jangan:** jelaskan kenapa, kasih konteks tambahan, atau spekulasi. Brief = instruksi, bukan edukasi.

## 5. Post-Flight

Setelah executor selesai → verifikasi:
- Output sesuai acceptance criteria?
- Ada residual risk?
- Report ke Boss: 3 baris — what, result, residual risk.

## Rules

- NEVER duplicate work. Once delegated, move on.
- Background tasks = FORBIDDEN. Semua foreground.
- Executor brief = MINIMAL. No fluff.
- Silent after dispatch? → WAIT. Jangan spam.
