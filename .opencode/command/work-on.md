---
description: Switch orchestrator context ke sub-project target — resolve path, baca sub-project.md, mulai kerja di folder itu.
agent: orchestrator
---

Boss mau pindah kerja ke sub-project: $ARGUMENTS

1. **Resolve path:**
- Kalau $ARGUMENTS adalah path absolut (C:\... atau /home/...) → pakai langsung.
- Kalau $ARGUMENTS adalah nama project (tanpa slash/backslash) → cari di `~/projects/<nama>` dulu, kalau nggak ada cari di `~/Documents/<nama>`.
- Kalau $ARGUMENTS adalah path relatif → resolve dari `~/projects/`.
- Kalau kosong → tanya Boss: "Project mana?"

2. **Set target root.** Semua agent (researcher/reviewer/executor) akan scoped ke path itu. Farewell-orchestra sendiri tetap safe — cuma target root yang digarap.

3. **Cek `sub-project.md`** di root target:
- Ada → baca, tampilin ringkasan ke Boss: ``` 🔄 Context: {PROJECT_NAME} 📁 Path: {path} 🎯 Fase: {phase} — {task aktif} ⚡ Profile: {paid|hybrid|free} ```
- Nggak ada → tanya Boss: "`sub-project.md` nggak ada. Mau gua scaffold `/new-project` dulu, atau langsung kerja aja tanpa docs?"

4. **Konfirmasi ke Boss:** "Siap kerja di {PROJECT_NAME}. Ada request?"

Catatan: Setelah context switch, ikuti orchestration rules normal (anti-gigo → decompose → parallel research/review → execute → report).
