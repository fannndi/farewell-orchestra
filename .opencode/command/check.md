---
description: Validate workspace readiness — personas, skills, profiles, connectivity. Run every new session.
agent: orchestrator
---

Validate the Farewell Orchestra workspace. Run these checks in order. Report PASS/FAIL for each.

## 1. Persona Files
Read and verify these files exist with valid YAML frontmatter:
- `.opencode/agents/orchestrator.md` — must have `name: orchestrator`, `mode: primary`
- `.opencode/agents/researcher.md` — must have `name: researcher`, `mode: subagent`
- `.opencode/agents/reviewer.md` — must have `name: reviewer`, `mode: subagent`
- `.opencode/agents/executor.md` — must have `name: executor`, `mode: subagent`

Report: "4/4 personas valid" or "X personas missing/invalid: ..."

## 2. Skills Directory
Count SKILL.md files in `skills/engineering/` and `skills/productivity/`.
Expected: ≥12 skills (engineering: ask-orchestrator, orchestrate, research-codebase, audit-security, implement-change, verify-profile, full-cycle, compound-review, grill-boss, setup-orchestra, writing-orchestra-skills; productivity: switch-profile, stress-test, handoff-session)

Report: "X/Y skills found. Missing: ..." (if any)

## 3. Profile Configs
Validate all 4 profile files are valid JSON:
- `profiles/opencode.paid.jsonc`
- `profiles/opencode.hybrid.jsonc`
- `profiles/opencode.free.jsonc`
- `profiles/opencode.free-backup.jsonc`

For each: check JSON parseable, has `agent.orchestrator`, `agent.executor`, provider.models populated.

Report: "4/4 profiles valid" or "X profiles FAIL: ..."

## 4. Environment
Check `.env` exists and contains `NINEROUTER_API_KEY` (don't print the key!).

Report: ".env OK" or ".env missing NINEROUTER_API_KEY"

## 5. Default Config
Verify root `opencode.jsonc` exists and is valid JSON.

Report: "opencode.jsonc OK" or "opencode.jsonc FAIL"

## 6. Summary
Format:
```
FAREWELL ORCHESTRA — Workspace Check
═══════════════════════════════════════
Personas:   [PASS/FAIL]
Skills:     [PASS/FAIL]
Profiles:   [PASS/FAIL]
Environment:[PASS/FAIL]
Config:     [PASS/FAIL]
═══════════════════════════════════════
Status: [READY / X issues found]
```

If READY: say "Orchestra siap. Profile aktif: {curret profile name}. Skill: {count} loaded."
If issues: list each issue in 1 line. Offer to fix automatically.
