---
name: grill
description: Use when anti-gigo finds input incomplete or ambiguous — Socratic interview one question at a time until shared understanding. Do NOT use when request is already clear.
---

> Role: read-only (kecuali executor). Writes → dispatch executor. Orchestrator never writes code.

# Grill-Me — Socratic Requirement Extraction

## Prinsip
- **Satu pertanyaan per satu waktu.** Jangan banjirin Boss. Satu `question` tool call = satu pertanyaan.
- **Fakta = cari sendiri.** Cari lewat read/grep/glob sebelum tanya Boss.
- **Keputusan = Boss.** Desain, arsitektur, trade-off → tanya Boss.

## Decision Tree — Walk Down Semua Cabang

| Level | Pertanyaan | Contoh |
|-------|-----------|--------|
| **Goal** | Apa yg mau dicapai? | "Fitur login" → login apa? User/admin? |
| **Scope** | Batasan? In/Out? | Register included? Forgot password? |
| **Constraints** | Tech stack? Deadline? | "Pake JWT atau session? Database apa?" |
| **Acceptance** | Gimana tau selesai? | "Test apa yg harus pass?" |
| **Risk** | Apa yg bisa gagal? | "Rate limit? Data breach vector?" |
| **Edge cases** | Input kosong? Concurrent? | "Multiple device login?" |

Jangan skip cabang. Tiap jawaban bisa buka cabang baru → gali terus sampai semua clear.

## Workflow
1. Orchestrator invoke grill setelah anti-gigo return PARTIAL (input punya goal tapi scope/acceptance/risk kurang).
2. Interview Boss — satu pertanyaan per waktu, tiap level decision tree, sampai semua clear.
3. **Sign-off** — summary decisions (≤5 bullets) + "Go / adjust?" prompt. Jangan fan-out sebelum sign-off.

## Proactive behavior

- Acceptance criteria kosong/vague → sub-agent WAJIB grill internal dulu (pakai decision tree), baru eksekusi.
- Ambiguitas baru muncul di tengah percakapan → grill Boss langsung, jangan tunda sampai akhir.

## Mantra

> "Lebih baik 10 pertanyaan sekarang daripada 100 baris kode yg salah nanti."
