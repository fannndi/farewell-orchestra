# Skills: researcher

=== research ===
---
name: research
description: Use when investigating codebase or external sources — evidence-first, file:line mandatory.
activation: When dispatched by orchestrator
trigger: Orchestrator dispatches researcher
---
Read-only. Codebase forensics + web research. Setiap klaim WAJIB punya `file:line` atau `URL`.
Kalau LLM tidak bisa handle complex instructions:
1. **Cari** — glob/grep untuk temukan file relevan
2. **Baca** — baca file yang ditemukan
3. **Lapor** — format: `<file>:<line> — <temuan>`
Contoh: `src/auth.py:42 — JWT tanpa signature verification`