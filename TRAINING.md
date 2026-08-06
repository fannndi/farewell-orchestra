# TRAINING.md

> Panduan training untuk LLM yang mengembangkan/mengoptimalkan Farewell Orchestra. Jalankan di awal sesi.

## Step 0 — Baca Ini Dulu (urutan WAJIB)

1. `.opencode/soul.md` — identitas + esensi
2. `README.md` — gambaran sistem
3. `AGENTS.md` — rules operasional
4. File ini — state + prioritas

**Uji pemahaman (kalau beda, baca ulang `.opencode/soul.md`):**
- FACTORY, bukan product. Output-nya yang harus KISS.
- Kompleksitas internal = deliberate. Jangan flag over-engineered tanpa evidence.
- Cost-agnostic: fokus kualitas, bukan hemat token.

## State Saat Ini (per 2026-08-07)

### Sudah Dikerjakan — JANGAN RE-KERJA
- [x] Instruksi di-slim 5 files (-32%)
- [x] Feedback loop: learn tool → Lessons
- [x] Testing: pytest 39 passed
- [x] Security: path traversal, .env read-deny
- [x] Verify stack: validate_output.py deleted, verify.py canonical
- [x] Skills 29→27 (merge 2)
- [x] README drift fix, Auto-Load, Freeze Rule
- [x] CI/CD: ci.yaml + test_integration fix
- [x] Warnings cleanup: pytest warnings
- [x] Memori sesi dicatat
- [x] Pipeline: test_pipeline.py + benchmark/stress
- [x] Consistency: 0 drift
- [x] Skill konsolidasi 27→18: 8 merge (implement←kiss-checklist,kiss-automation; anti-patterns←simplification; code-review←quality-gates; research←edge-cases; feedback-loop←agent-monitor; task-decomposer←task-priority; orchestrate←agent-protocol; bootstrap-project←project-type-detection)
- [x] Persona upgrade: 4 agent punya karakter (Kapten/Detektif/Auditor/Tukang) + tabel Keahlian WAJIB PAKAI (skill harus di-load kalau kondisi trigger terpenuhi)
- [x] Benchmark data-driven: scripts/benchmark.py ngukur context budget per model tier (MUST/CORE/PIPELINE/ON-DEMAND), bukan asumsi 2000
- [x] Precision pass: 28 additions ke 5 skill inti (implement/research/review/prepare/orchestrate) + 16 ke 4 persona — hapus ambiguitas (LEVEL selection, BLOCKING matrix, D1-D3 depth, verify gate threshold, KISS before/after example, dll)
- [x] Restore README (71→116 lines: Skills table, Agents table, Project Structure, Automation Scripts) — reversal over-slim, presisi > hemat
- [x] Cleanup sinergi: delete workflows/cross-project.md (duplicate cross-project/guide.md), protocols/agent-communication.md (stale), snapshots/ (empty); fix generate.py duplicate watcher
- [x] Reminder "Presisi > Brevity" di `.opencode/soul.md` + AGENTS.md + TRAINING.md — cost urusan Boss, jangan korbankan presisi

### Prioritas Terbuka (pilih 1-2 per sesi)
1. **Rotate API key** — `.env` masih key lama (butuh Boss)
2. **Runtime stress test** — tiap role model beda (switch profile)
3. **Context budget dimanfaatkan untuk presisi** — benchmark.py ngukur per model tier; instruksi bukan bottleneck (load max ~20K = 15.5% dari 128K). Arah: tambah presisi (bukan slim) kalau ada gap; optimasi tool output pruning/compaction untuk task context

## Aturan Main Training

- **KISS** — factory boleh kompleks; over-engineered wajib evidence.
- **Tidak skip test/verify** — wajib di-test + di-verify.
- **Tidak ngarang** — kalau nggak tau, bilang.
- **Cost-agnostic** — fokus kualitas.
- **Presisi > Brevity** — Hapus verbosity, bukan rules/examples. Context budget besar, jangan slim rules demi hemat. Cost urusan Boss.
- **Feedback loop** — insiden → learn tool.
- **Satu perubahan, satu verify** — jangan menumpuk.

## Verifikasi Selesai

- [ ] pytest pass (`python -m pytest tests/ -q`)
- [ ] Perubahan diverifikasi, bukan cuma "should work"
- [ ] Lesson dicatat kalau insiden
- [ ] TRAINING.md state di-update
