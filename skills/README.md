# Farewell Orchestra — Skills

Skills that make the 4-agent orchestra smarter. Organized into buckets:

| Bucket | Purpose | Skills |
|--------|---------|--------|
| [engineering/](engineering/) | Daily code work — model + user invoked | orchestrate, research-codebase, audit-security, implement-change, verify-profile, ask-orchestrator, grill-boss, full-cycle, compound-review, setup-orchestra, writing-orchestra-skills |
| [productivity/](productivity/) | Workflow tools — model + user invoked | switch-profile, stress-test, handoff-session |

## Model-invoked Skills

| Skill | Description | Agent |
|-------|-------------|-------|
| [switch-profile](productivity/switch-profile/SKILL.md) | Orchestrator-triggered profile switching — Boss expresses intent, not commands | orchestrator |
| [stress-test](productivity/stress-test/SKILL.md) | Orchestrator-triggered 6-test stress suite — Boss says "test all profiles" | orchestrator |
| [orchestrate](engineering/orchestrate/SKILL.md) | Decompose, fan-out, synthesize, delegate | orchestrator |
| [research-codebase](engineering/research-codebase/SKILL.md) | Forensic codebase investigation with file:line evidence | researcher |
| [audit-security](engineering/audit-security/SKILL.md) | STRIDE-based security + architecture audit | reviewer |
| [implement-change](engineering/implement-change/SKILL.md) | YAGNI-driven minimal implementation + DoD gate | executor |
| [verify-profile](engineering/verify-profile/SKILL.md) | Validate opencode.jsonc config integrity (15 checks) | all |
| [full-cycle](engineering/full-cycle/SKILL.md) | Complete pipeline — decompose → fan-out → implement → verify | orchestrator |
| [compound-review](engineering/compound-review/SKILL.md) | Multi-axis parallel review for significant changes (>50 lines) | reviewer |

## User-invoked Skills

| Skill | Description | Agent |
|-------|-------------|-------|
| [ask-orchestrator](engineering/ask-orchestrator/SKILL.md) | Router skill — maps all skills and their chain relationships | user |
| [grill-boss](engineering/grill-boss/SKILL.md) | Clarify ambiguous requests — one question at a time | user |
| [handoff-session](productivity/handoff-session/SKILL.md) | Save session state for cross-session resume | orchestrator |
| [setup-orchestra](engineering/setup-orchestra/SKILL.md) | One-shot validation of entire Orchestra setup | orchestrator |
| [writing-orchestra-skills](engineering/writing-orchestra-skills/SKILL.md) | Meta-skill — how to write Farewell Orchestra skills | user |
