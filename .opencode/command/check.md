# Farewell Orchestra — Health Check

## 1. Core files

- [ ] opencode.jsonc — valid JSON, ada `agent.orchestrator`
- [ ] AGENTS.md — ada, tidak kosong
- [ ] .opencode/agents/orchestrator.md — ada
- [ ] .opencode/agents/researcher.md — ada
- [ ] .opencode/agents/reviewer.md — ada
- [ ] .opencode/agents/executor.md — ada

## 2. Skills (6 file di .opencode/skills/)

- [ ] prepare — input validation + cross-project detection + chunking
- [ ] orchestrate — decompose + fan-out + synthesize
- [ ] research — codebase + web research
- [ ] review — STRIDE audit
- [ ] implement — YAGNI + verify
- [ ] bootstrap-project — scaffold docs (5+2)

## 3. Cross-project guide

- [ ] cross-project/guide.md — ada, workflow jelas
- [ ] templates/sub-project.md — ada, format 5+2 docs

## 4. Profile system

- [ ] profiles/profiles.json — valid JSON
- [ ] profiles/generate.py — bisa generate
- [ ] `python profiles/generate.py --validate` — semua profile valid

## 5. Profile aktif

- [ ] Model assignments bener — cek `opencode.jsonc.agent.*.model`
- [ ] Skill-load prompts — 3 sub-agent (researcher/reviewer/executor) harus ada instruksi skill-load
- [ ] Instructions — cuma AGENTS.md

## 6. Custom tools

- [ ] .opencode/tools/verify.ts + verify.py — verification gate
- [ ] .opencode/tools/harness_status.ts — health check
- [ ] .opencode/tools/learn.ts — lesson logger

## Result

Semua checkboxes harus [PASS]. Kalau ada [FAIL] → perlu sync.
