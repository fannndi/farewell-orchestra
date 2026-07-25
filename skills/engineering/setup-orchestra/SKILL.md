---
name: setup-orchestra
description: Use when setting up Farewell Orchestra for the first time, or when something seems broken. Validates all 4 profiles, persona files, skills directory, and 9Router connectivity.
disable-model-invocation: true
---

## Purpose

One-shot validation of the entire Farewell Orchestra setup. Run this before your first session, after pulling updates, or when something seems off. Catches misconfiguration before it wastes tokens.

## What It Validates

### Profiles (4 files)
- [ ] `profiles/opencode.paid.jsonc` — exists, valid JSON, 15/15 checks
- [ ] `profiles/opencode.hybrid.jsonc` — exists, valid JSON, 15/15 checks
- [ ] `profiles/opencode.free.jsonc` — exists, valid JSON, 15/15 checks
- [ ] `profiles/opencode.free-backup.jsonc` — exists, valid JSON, 15/15 checks
- [ ] `opencode.jsonc` — default config sync'd with paid

### Personas (4 files)
- [ ] `.opencode/agents/orchestrator.md` — exists, valid frontmatter
- [ ] `.opencode/agents/researcher.md` — exists, valid frontmatter
- [ ] `.opencode/agents/reviewer.md` — exists, valid frontmatter
- [ ] `.opencode/agents/executor.md` — exists, valid frontmatter

### Skills (14 files)
- [ ] `skills/engineering/orchestrate/SKILL.md`
- [ ] `skills/engineering/research-codebase/SKILL.md`
- [ ] `skills/engineering/audit-security/SKILL.md`
- [ ] `skills/engineering/implement-change/SKILL.md`
- [ ] `skills/engineering/verify-profile/SKILL.md`
- [ ] `skills/engineering/ask-orchestrator/SKILL.md`
- [ ] `skills/engineering/grill-boss/SKILL.md`
- [ ] `skills/engineering/full-cycle/SKILL.md`
- [ ] `skills/engineering/compound-review/SKILL.md`
- [ ] `skills/engineering/setup-orchestra/SKILL.md`
- [ ] `skills/engineering/writing-orchestra-skills/SKILL.md`
- [ ] `skills/productivity/switch-profile/SKILL.md`
- [ ] `skills/productivity/stress-test/SKILL.md`
- [ ] `skills/productivity/handoff-session/SKILL.md`

### Connectivity
- [ ] `.env` contains NINEROUTER_API_KEY
- [ ] 9Router reachable at 127.0.0.1:20128

## Process

1. Run all profile validations via `verify-profile` skill
2. Check all persona files exist with valid frontmatter
3. List all skills — confirm 14 SKILL.md files present
4. Check .env exists with API key (don't print the key!)
5. Ping 9Router health endpoint
6. Report: "X/Y checks passed. Z issues found."

## Rules

- One FAIL → report immediately with fix instructions
- All PASS → "Setup complete. 15/15 across all profiles. Ready to orchestrate."
- Never print API keys or secrets in output

## Failure Modes

- **Partial validation** — checking profiles but skipping skills. Everything matters.
- **Leaked secrets** — printing the API key in the report. Mask it.
- **False PASS** — assuming files exist without actually reading them. Verify content, not just path.
