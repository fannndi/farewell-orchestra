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
- [ ] Cek `compaction.prune_rules` — ada kalau `prune: true`

## 5. Persona skills frontmatter

- [ ] Setiap agent file punya `skills:` key dan file skill-nya ada

## 6. Custom tools

- [ ] .opencode/tools/verify.ts + verify.py — verification gate
- [ ] .opencode/tools/harness_status.ts — health check
- [ ] .opencode/tools/learn.ts — lesson logger

## Result

Semua checkboxes harus ✅. Kalau ada ❌ → perlu sync.
