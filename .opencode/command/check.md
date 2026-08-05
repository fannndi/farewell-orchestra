# Farewell Orchestra — Health Check

Run on every new session. Validasi struktur workspace + profile.

## 1. Core files

- [ ] opencode.jsonc — valid JSON, ada `agent.orchestrator`
- [ ] AGENTS.md — ada, tidak kosong
- [ ] project-guide.md — ada
- [ ] Farewell-Knowlage/Lessons.md — ada (Obsidian vault)
- [ ] .opencode/agents/orchestrator.md — ada
- [ ] .opencode/agents/researcher.md — ada
- [ ] .opencode/agents/reviewer.md — ada
- [ ] .opencode/agents/executor.md — ada

## 2. Skills (11 file di .opencode/skills/)

- [ ] anti-gigo, grill, orchestrate, forensic, web-research — ada
- [ ] stride-audit, minimal-impl, verification-ground-truth — ada
- [ ] bootstrap-project, synthesis-brief — ada

## 3. Profile system

- [ ] profiles/profiles.json — valid JSON, ada models + profiles
- [ ] profiles/generate.py — bisa generate profile
- [ ] profiles/opencode.temp.jsonc — auto-generated (di-gitignore)
- [ ] profiles/opencode.example.jsonc — contoh hasil generate
- [ ] switch.bat — bisa panggil generate.py --menu

## 4. Profile aktif

- [ ] Model assignments bener — cek `opencode.jsonc.agent.*.model` (hasil generate.py)
- [ ] `python profiles/generate.py --validate` — semua profile valid
- [ ] Step budget — BACA dari `opencode.jsonc.agent.<name>.steps` (jangan hardcode)
  - Minimum sanity floor = 20 (atau 80% dari declared, mana yang lebih tinggi)
- [ ] Cek `instructions` — cuma AGENTS.md (gak load *.md semua)
- [ ] Skill-load prompts — 3 sub-agent (researcher/reviewer/executor) harus ada instruksi skill-load: grep "WAJIB: di awal task" di opencode.jsonc (atau generate.py) → minimal 3 match. Kalau kurang → warning
- [ ] Cek `compaction.prune_rules` — ada kalau `prune: true`

## 5. Persona skills frontmatter

- [ ] Setiap agent file punya `skills:` key dan file skill-nya ada

## 6. Custom tools

- [ ] .opencode/tools/verify.ts + verify.py — verification gate
- [ ] .opencode/tools/harness_status.ts — health check: `@harness_status check:"all" format:"json"`
  - JSON output fields: `profile` (opencode.jsonc.model) · `agents.*.model` + `steps_limit` (opencode.jsonc.agent.*) · `profiles.valid` (via `generate.py --validate`) · `sensors` (count [PASS]/[FAIL]/[WARN] di `Lessons.md` ## Sensor Coverage — manual/periodik, bukan otomatis) · `errors` · `healthy` (true = no errors)
- [ ] .opencode/tools/learn.ts — lesson logger

## 7. Feature maturity — Declared→Wired→Exercised→Verified

Checklist for every custom tool / mechanism:

| Tool | [D] Declared | [W] Wired | [E] Exercised | [V] Verified |
|------|:---:|:---:|:---:|:---:|
| verify.ts | check.md | `AGENTS.md` § Trust & Dispatch (Verify gate) | sesi real | generate.py --validate |
| harness_status.ts | check.md | `check.md` § 6 | sesi real | `@harness_status` |
| learn.ts | check.md | `AGENTS.md` § Emergency Protocol (log via executor) | sesi real | cek Farewell-Knowlage/Lessons.md row |
| bash_denylist | generate.py | `.opencode/hooks/post-generate.ps1`:29-30 | generate.py hook | `python generate.py default` |
| step budget scaling | `AGENTS.md` § Step Budgets | `AGENTS.md` § Step Budgets | dispatch tiap task | cek langkah terpakai vs batas |

**Legend:** [D] ada di doc/config | [W] agent/skill instructions nyebut | [E] pernah dipanggil | [V] ada cara verify

## 8. Doc Link Integrity Checker

Manual check — tidak ada auto-trigger via hooks/CI:

- **Script:** `.opencode/scripts/check-links.py` — melacak semua refs di markdown
- **Coverage:** Formal links (text diikuti path dalam kurung), refs seperti `filename.md` dan `filename.md:42`
- **Forward refs:** file yang akan dihasilkan oleh bootstrap-project (sub-project.md, PRD.md, dsb.) dikecualikan
- **Trigger:** hooks.jsonc dispatches link-check via `beforeCommit` handler (check-links hook). Also runnable manually:
- **Exit code:** 0 kalau semua beres, 1 kalau ada broken references
- **Output:** `[LINK-CHECK] Scanning <N> markdown files...` + report per broken ref format `  BROKEN <rel>:<line> — <target> -> NOT FOUND`

Verifikasi:
- Run `python .opencode/scripts/check-links.py`

Hasil expected:
- `[LINK-CHECK] Scanning <N> markdown files...`
- `[LINK-CHECK] OK — <X> references verified (<Y> links, <Z> file refs), 0 broken`

Kalau gagal:
- Report broken refs ke revision list
- Run `git log --grep="doc` untuk wisata changelog terakhir
- Edit file yang rusak atau perbaiki link yang rusak

## Result

Semua checkboxes harus [PASS]. Kalau ada [FAIL] → perlu sync.
