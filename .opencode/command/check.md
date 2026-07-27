# Farewell Orchestra — Health Check

Run on every new session. Validasi struktur workspace.

## 1. Core files

- [ ] opencode.jsonc — valid JSON, ada `agent.orchestrator`
- [ ] AGENTS.md — ada, tidak kosong
- [ ] .opencode/agents/orchestrator.md — ada
- [ ] .opencode/agents/researcher.md — ada
- [ ] .opencode/agents/reviewer.md — ada
- [ ] .opencode/agents/executor.md — ada

## 2. Skills (8 file di .opencode/skills/)

- [ ] .opencode/skills/anti-gigo/SKILL.md — ada
- [ ] .opencode/skills/orchestrate/SKILL.md — ada
- [ ] .opencode/skills/forensic/SKILL.md — ada
- [ ] .opencode/skills/web-research/SKILL.md — ada
- [ ] .opencode/skills/stride-audit/SKILL.md — ada
- [ ] .opencode/skills/minimal-impl/SKILL.md — ada
- [ ] .opencode/skills/verification-ground-truth/SKILL.md — ada
- [ ] .opencode/skills/bootstrap-project/SKILL.md — ada

## 3. Profiles (3 file)

- [ ] profiles/opencode.paid.jsonc — valid JSON, 4 agents
- [ ] profiles/opencode.hybrid.jsonc — valid JSON, 4 agents
- [ ] profiles/opencode.free.jsonc — valid JSON, 4 agents

## 4. Persona skills frontmatter

- [ ] .opencode/agents/orchestrator.md — punya `skills:` key
- [ ] .opencode/agents/researcher.md — punya `skills:` key
- [ ] .opencode/agents/reviewer.md — punya `skills:` key
- [ ] .opencode/agents/executor.md — punya `skills:` key

## 5. Consistency

- [ ] opencode.jsonc steps match profiles/opencode.paid.jsonc steps
- [ ] README 3 profiles section match actual profile count
- [ ] Tidak ada file ketinggalan dari arsitektur lama (paid-limit, free-backup)

## Result

Semua checkboxes di atas harus ✅. Kalau ada yang ❌ → workspace stale, perlu sync.
