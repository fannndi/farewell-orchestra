---
name: verify-profile
description: Use when validating opencode.jsonc configuration. Runs 15 checks on config integrity, permission security, and model failover.
---

## Purpose

Validate any opencode profile config against the 15-point checklist covering config integrity, permission security, and model failover. Used by all agents when loading or switching profiles.

## Trigger

Invoke this skill when:
- Loading a new profile (`opencode -c profiles/opencode.*.jsonc`)
- After modifying any opencode.jsonc file
- During stress-test workflow (pre-executor checkpoint)
- Boss asks "verify config" or "is this profile valid?"

## 15-Point Checklist

### Config Integrity (5 checks)
1. JSON/JSONC syntax valid?
2. All agent.model refs exist in provider.models?
3. Orchestrator has `"*": "deny"` in permission?
4. Executor has `"*": "deny"` in permission + `"temperature": 0.2`?
5. General + explore have explicit deny-by-default permissions?

### Permission Security (5 checks)
6. General + explore define `"*": "deny"` + explicit read/glob/grep/list + `"task": "deny"`?
7. Compaction agent has `"steps": 10` + appropriate model tier?
8. All 4 core agents have: mode, model, prompt, permission, temperature, steps?
9. Provider has required fields: name, npm, env, options, models?
10. No duplicate agent names?

### Model Failover (5 checks)
11. `subagent_depth: 1` present?
12. Compaction `auto/prune/tail_turns` present?
13. Experimental/watcher/attachment/lsp/formatter present?
14. Compaction model tier appropriate for profile (not pro on paid)?
15. All model keys in agent.model match exact key in provider.models?

## Rules

- Verify ALL profiles present: paid, hybrid, free, free-backup, default (opencode.jsonc)
- Report PASS/FAIL per check per profile
- One critical FAIL → BLOCKING. Report immediately.
- All PASS → "15/15" confirmation

## Failure Modes

- **Partial check** — verifying 3 profiles but not all 5. Complete the set.
- **False positive** — "model refs match" without checking the actual provider.models keys. String-match exactly.
- **Missing default** — only verifying the 4 named profiles. opencode.jsonc in root must also pass.
