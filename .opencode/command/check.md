# Farewell Orchestra — Health Check

Run on every new session. Validasi struktur workspace + profile.

## 1. Core files

- [ ] opencode.jsonc — valid JSON, ada `agent.orchestrator`
- [ ] AGENTS.md — ada, tidak kosong
- [ ] project-guide.md — ada
- [ ] LESSONS.md — ada
- [ ] .opencode/agents/orchestrator.md — ada
- [ ] .opencode/agents/researcher.md — ada
- [ ] .opencode/agents/reviewer.md — ada
- [ ] .opencode/agents/executor.md — ada

## 2. Skills (9 file di .opencode/skills/)

- [ ] anti-gigo, grill, orchestrate, forensic, web-research — ada
- [ ] stride-audit, minimal-impl, verification-ground-truth — ada
- [ ] bootstrap-project — ada

## 3. Profile system

- [ ] profiles/profiles.json — valid JSON, ada models + profiles
- [ ] profiles/generate.py — bisa generate profile
- [ ] profiles/opencode.temp.jsonc — auto-generated (di-gitignore)
- [ ] profiles/opencode.example.jsonc — contoh hasil generate
- [ ] switch.bat — bisa panggil generate.py --menu

## 4. Profile aktif

- [ ] `python profiles/generate.py --inspect <active>` — model assignments bener
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
- [ ] .opencode/tools/harness_status.ts — health check
- [ ] .opencode/tools/learn.ts — lesson logger

## 7. Feature maturity — Declared→Wired→Exercised→Verified

Checklist for every custom tool / mechanism:

| Tool | [D] Declared | [W] Wired | [E] Exercised | [V] Verified |
|------|:---:|:---:|:---:|:---:|
| verify.ts | check.md | `.opencode/agents/orchestrator.md`:22-30 | sesi real | generate.py --validate |
| harness_status.ts | check.md | `.opencode/agents/orchestrator.md`:62-64 | sesi real | `@harness_status` |
| learn.ts | check.md | `.opencode/agents/orchestrator.md`:69 | sesi real | cek LESSONS.md row |
| bash_denylist | generate.py | `.opencode/hooks/post-generate.ps1`:29-30 | generate.py hook | `python generate.py default-oc` |
| step budget scaling | `.opencode/agents/orchestrator.md`:38-48 | `.opencode/agents/orchestrator.md`:48 | dispatch tiap task | bandingkan actual vs budget |

**Legend:** [D] ada di doc/config | [W] agent/skill instructions nyebut | [E] pernah dipanggil | [V] ada cara verify

## 8. Doc Link Integrity Checker

Manual check — tidak ada auto-trigger via hooks/CI:

- **Script:** `.opencode/scripts/check-links.py` — melacak semua refs di markdown
- **Coverage:** Formal links (text diikuti path dalam kurung), refs seperti `filename.md` dan `filename.md:42`
- **Forward refs:** file yang akan dihasilkan oleh bootstrap-project (sub-project.md, PRD.md, dsb.) dikecualikan
- **Trigger:** HANYA manual — hooks.jsonc tidak dispatch event link-check (tidak ada `sessionEnd`/`beforeCommit` handler). Jalankan langsung:
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
