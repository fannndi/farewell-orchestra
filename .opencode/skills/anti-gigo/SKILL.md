---
name: anti-gigo
description: Use when receiving user request — validate input quality, enforce brief framework, detect trash before dispatch
---

# Anti-GIGO: Garbage In → Garbage Out

**Prinsip:** AI model termahal pun hasilkan sampah kalau inputnya sampah. AI bukan cenayang — dia over-interpolasi, over-engineer, dan context drift kalau input nggak jelas. Skill ini adalah gerbang kualitas sebelum satu token pun terbuang ke downstream.

## 1. Brief Framework Validator

Setiap request WAJIB punya 4 elemen sebelum dispatch:

| Elemen | Wajib | Kalau kosong |
|--------|-------|-------------|
| **Goal** | ✅ | STOP. Tanya: "Goal-nya apa?" (1 kalimat) |
| **Scope** | ✅ | STOP. Tanya: "File/folder mana?" |
| **Acceptance** | ✅ | Usulkan 1 cara test, minta konfirmasi |
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
🤔 Asumsi:
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
| TRIVIAL | 1 file, ≤3 step, reversible | DIRECT execute |
| MEDIUM | 1-3 files, >3 step, reversible | Researcher + executor |
| COMPLEX | >3 files, irreversible | FULL orchestra |

Kalau ragu → naikkan 1 kelas.

## Output

Kalau input CLEAN → `PASS. [TRIVIAL|MEDIUM|COMPLEX]. Lanjut orchestrate.`

Kalau input TRASH → `HOLD. [alasan]. Tanya: [pertanyaan 1 kalimat].`
