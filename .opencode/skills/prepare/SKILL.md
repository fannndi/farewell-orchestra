---
name: prepare
description: Use when receiving a request — validate input, extract requirements, chunk if needed. Gate before orchestration.
---

# Prepare

Gate awal sebelum dispatch. Flow:

```
Request → Input Validation → HOLD? STOP. PARTIAL? → Grill. PASS? → Chunk → Dispatch
```

## 1. Input Validation

Cek request punya 4 elemen:

| Elemen | Wajib | Kalau kosong |
|--------|-------|-------------|
| **Goal** | YA | STOP. Tanya: "Goal-nya apa?" |
| **Scope** | YA | STOP. Tanya: "File/folder mana?" |
| **Acceptance** | YA | Usulkan 1 cara test, minta konfirmasi |
| **Risk** | Default LOW | Pakai LOW kalau tidak disebut |

**Trash detection** — STOP + clarify kalau:
- <10 kata tanpa konteks ("perbaikin", "tambahin")
- Ambigu multi-interpretasi ("benerin itu")
- Kontradiktif dalam satu request
- Scope liar ("refactor semuanya") tanpa batasan

**Output decision:**
- `HOLD [alasan]` → STOP. Tanya Boss.
- `PARTIAL` → lanjut ke §2 Assumption Logger, lalu §3 Grill.
- `PASS [SIZE]` → lanjut ke §4 Task Chunking.

Size: TRIVIAL (1 file, ≤3 baris) / SMALL (1-2 files) / MEDIUM (3-5 files) / LARGE (>5 files)

## 2. Assumption Logger

Hanya kalau PARTIAL. Auto-generate asumsi implisit, max 3:

```
Asumsi:
1. [asumsi 1] — ok?
2. [asumsi 2] — ok?
```

Boss reply `1:ya 2:tidak → pakai X` atau `semua ok`.

**Rubber-stamp guard:** Kalau Boss bilang "ok" ke semua asumsi tanpa edit → flag: "Asumsi belum dikonfirmasi. Konfirmasi 1 per 1?" Jangan lanjut kalau asumsi belum benar-benar dikonfirmasi.

## 3. Requirement Extraction (Grill)

Hanya kalau PARTIAL setelah Assumption Logger. Interview Boss satu pertanyaan per waktu:

| Level | Pertanyaan |
|-------|-----------|
| Goal | Apa yang mau dicapai? |
| Scope | Batasan? In/Out? |
| Constraints | Tech stack? Deadline? |
| Acceptance | Gimana tau selesai? |
| Risk | Apa yang bisa gagal? |
| Edge cases | Input kosong? Concurrent? |

Satu `question` tool call = satu pertanyaan. Max 8 pertanyaan, lalu sign-off paksa dengan asumsi default.

**Pendulum Check:** Over-spec (10 library, 5 pattern) → tanya "Prioritas?". Under-spec (terlalu umum) → paksa "Contoh input/output?"

## 4. Task Chunking

Trigger chunk kalau: **Q≥3** (pertanyaan) ATAU **F≥3** (file) ATAU **O≥2** (format output).

| Size | Action |
|------|--------|
| TRIVIAL/SMALL | 1 chunk, fan-out normal |
| LARGE | 2-3 chunk |
| MASSIVE | 3-4 chunk |

Per chunk: ≤2 file, 1 fokus, 1 format. **DALAM chunk:** parallel. **ANTAR chunk:** sequential dengan CONTEXT_SUMMARY.

Sub-agent boleh return `[CHUNK_REQUIRED]` kalau task kegedean → re-chunk, bukan gagal.
