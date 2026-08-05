---
name: anti-gigo
description: Use when receiving a user request — validate input quality, enforce brief framework, detect trash before dispatch.
---

> Role: read-only (kecuali executor). Writes → dispatch executor. Orchestrator never writes code.

# Anti-GIGO: Garbage In → Garbage Out

**Prinsip:** AI model sehebat apapun pun hasilkan sampah kalau inputnya sampah. AI bukan cenayang — dia over-interpolasi, over-engineer, dan context drift kalau input nggak jelas. Skill ini adalah gerbang kualitas sebelum sampah terproses ke downstream.

## 1. Brief Framework Validator

Setiap request WAJIB punya 4 elemen sebelum dispatch:

| Elemen | Wajib | Kalau kosong |
|--------|-------|-------------|
| **Goal** | [PASS] | STOP. Tanya: "Goal-nya apa?" (1 kalimat) |
| **Scope** | [PASS] | STOP. Tanya: "File/folder mana?" |
| **Acceptance** | [PASS] | Usulkan 1 cara test, minta konfirmasi |
| **Risk** | Default LOW | Pakai LOW kalau Boss tidak sebut |

## 2. Trash Detector

Trigger **STOP + clarify** kalau:

- **Terlalu pendek:** <10 kata, tanpa konteks (`"perbaikin"`, `"tambahin"`)
- **Ambigu:** multi-interpretasi (`"benerin itu"`, `"update aja"`)
- **Kontradiktif:** dua instruksi bertentangan dalam satu request
- **Scope liar:** `"refactor semuanya"`, `"audit semua file"` tanpa batasan
- **Missing dependency:** sebut file tapi nggak kasih path

## 3. Assumption Logger

Auto-generate asumsi implisit sebelum dispatch. Max 3. Konfirmasi ke Boss:

```
Asumsi:
1. [asumsi 1] — ok?
2. [asumsi 2] — ok?
```

Boss reply `1:ya 2:tidak → pakai X` atau `semua ok`.

## 4. Pendulum Check

Tiap request → klasifikasi ekstrem:
- **Over-spec:** detail berlebihan (sebut 10 library, 5 pattern) → tanya: "Prioritas?"
- **Under-spec:** terlalu umum → paksa konkret: "Contoh input/output?"

## 5. Cost-Benefit Gate

| Kelas | Kriteria | Tindakan |
|-------|----------|----------|
| TRIVIAL | 1 file, ≤3 baris, no blast | Researcher + executor (reviewer optional) — orchestrator never writes code, always delegate |
| SMALL | 1-2 files, ≤20 baris, low blast | Researcher + executor |
| MEDIUM | 3-5 files, low-medium blast | Researcher + executor |
| LARGE | >5 files atau high blast | FULL orchestra |
| MASSIVE | Full audit + refactor multi-module | FULL orchestra |

Kalau ragu → naikkan 1 kelas.

## Output

Kalau input CLEAN → `PASS. [TRIVIAL|SMALL|MEDIUM|LARGE|MASSIVE]. Lanjut orchestrate.`

Kalau input INCOMPLETE (ada goal tapi scope/acceptance/risk kurang, bukan full trash) → `PARTIAL. Recommend grill.`

Kalau input TRASH (no goal, no scope, <10 kata) → `HOLD. [alasan]. Tanya: [pertanyaan 1 kalimat].`

## Proactive behavior

- Sub-agent (researcher/reviewer/executor) yang nerima task ambigu/partial → WAJIB invoke anti-gigo internal: minta revisi brief ke orchestrator. JANGAN coba tebak.
- Anti-gigo bukan cuma gerbang orchestrator — berlaku di semua role yang nerima input. Clear in, clear out.
