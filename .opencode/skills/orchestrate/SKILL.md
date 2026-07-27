---
name: orchestrate
description: Use after anti-gigo passes — decompose request, fan-out parallel, synthesize results, delegate to executor
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
- Conflict? → reviewer (security audit) > researcher (code facts). Tapi kalau researcher punya bukti konkret (file:line) yang membantah reviewer → catat sebagai "dispute" dan present ke Boss, jangan resolve sendiri.
- Siapkan executor brief dari hasil sintesis

## 4. Delegate — Structured Handoff Brief

Tiap brief ke sub-agent WAJIB 5 field ini, max 200 token total:

```
TASK: [1 kalimat — apa yg harus dihasilkan]
FILES: [path, path — file yg disentuh]
CONTEXT: [1-2 kalimat — kenapa, constraint spesifik]
TRIED: [opsional — apa yg udah dicoba & gagal, biar nggak diulang]
VERIFY: [command — cara test bahwa task selesai]
```

**Jangan:** jelaskan kenapa panjang, kasih konteks tambahan, spekulasi, "mungkin kamu perlu...", "coba lihat juga...". Brief = instruksi presisi, bukan mentoring.

## 5. Post-Flight

Setelah executor selesai → verifikasi:
- Output sesuai acceptance criteria?
- Ada residual risk?
- Report ke Boss: 3 baris — what, result, residual risk.

6. **Escalation:** executor gagal 2x → STOP. Jangan dispatch executor lagi. Dispatch researcher dengan brief: "Deep debug [error]. Root cause, bukan symptom." Researcher invoke `forensic`.

## 7. Peer Debate Mode (high-stakes correctness)

Kalau Boss minta verifikasi ekstra atau task high-stakes (auth, keamanan, data integrity):

1. **Researcher** → analisis codebase, temukan fakta (evidence file:line)
2. **Reviewer** → critique findings researcher, tunjuk celah atau missing evidence
3. **Researcher (rebuttal)** → tanggapi critique dengan bukti tambahan atau akui kalau reviewer benar
4. **Synthesize** → orchestrator gabungkan final conclusion

**Token efficiency:** Saat researcher rebuttal, GUNAKAN `task_id` dari dispatch researcher pertama — resume subagent, bukan dispatch ulang dari nol. Researcher bawa full history sendiri, nggak perlu re-brief. Ini bypass 200-token cap karena context sudah ada dari sesi sebelumnya.

Trigger: Boss bilang `debat` atau `double check` atau `pastiin bener`. Atau orchestrator deteksi task nyangkut auth/security/data-loss.

Output format:
```
✅ AGREED: [poin yg researcher & reviewer sepakat]
⚠️ DEBAT: researcher klaim X (path:42), reviewer counter Y — [resolusi]
📋 FINAL: [kesimpulan setelah debate]
```

## Rules

- NEVER duplicate work. Once delegated, move on.
- Background tasks = FORBIDDEN. Semua foreground.
- Executor brief = MINIMAL. No fluff.
- Silent after dispatch? → WAIT. Jangan spam.

## 6. Loop Guard

Deteksi loop sebelum buang token:

| Sinyal loop | Action |
|-------------|--------|
| Agent + tool + intent sama terulang 3x berturut-turut | STOP. Jangan dispatch lagi. |
| Executor gagal dengan error identik 2x | Escalate ke researcher, jangan retry executor |
| Researcher balikin hasil yg sama 2x | Udah cukup — synthesize, jangan research lagi |
| Conversation muter di topik yg sama tanpa progress | Report ke Boss: "Stuck di [topik]. Perlu arahan." |

**Prinsip:** 3x sama = loop. Token lebih baik buat nanya Boss daripada muter di tempat.
