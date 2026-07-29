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

## 3. Profiles (6 file)

- [ ] profiles/opencode.default.jsonc — valid JSON
- [ ] profiles/opencode.default-or.jsonc — valid JSON
- [ ] profiles/opencode.ollama.jsonc — valid JSON
- [ ] profiles/opencode.ollama-or.jsonc — valid JSON
- [ ] profiles/opencode.codex.jsonc — valid JSON
- [ ] profiles/opencode.codex-or.jsonc — valid JSON

## 4. Profile aktif

- [ ] Cek opencode.jsonc `model` field — profile mana yg aktif
- [ ] Step budget: orchestrator 20 / researcher 18 / reviewer 14 / executor 18
- [ ] Cek `instructions` — ada AGENTS.md

## 5. Persona skills frontmatter

- [ ] Setiap agent file punya `skills:` key dan file skill-nya ada

## 6. Test scripts

- [ ] test/test_models.bat — ada
- [ ] test/test_or_models.bat — ada
- [ ] test/test_codex.bat — ada

## Result

Semua checkboxes harus ✅. Kalau ada ❌ → perlu sync.
