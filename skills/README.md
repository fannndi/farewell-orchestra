# Farewell Orchestra — Skills

Skills that make the 4-agent orchestra smarter. Organized into buckets:

| Bucket | Purpose | Skills |
|--------|---------|--------|
| [engineering/](engineering/) | Daily code work — invoked by models | orchestrate, research-codebase, audit-security, implement-change, verify-profile |
| [productivity/](productivity/) | Workflow tools — invoked by user | switch-profile, stress-test |

## User-invoked Skills

| Skill | Description |
|-------|-------------|
| [switch-profile](productivity/switch-profile/SKILL.md) | Guided profile switching between paid/hybrid/free/free-backup |
| [stress-test](productivity/stress-test/SKILL.md) | Trigger the full 6-test orchestration stress suite |

## Model-invoked Skills

| Skill | Description | Agent |
|-------|-------------|-------|
| [orchestrate](engineering/orchestrate/SKILL.md) | Decompose, fan-out, synthesize, delegate | orchestrator |
| [research-codebase](engineering/research-codebase/SKILL.md) | Forensic codebase investigation with file:line evidence | researcher |
| [audit-security](engineering/audit-security/SKILL.md) | STRIDE-based security + architecture audit | reviewer |
| [implement-change](engineering/implement-change/SKILL.md) | YAGNI-driven minimal implementation + DoD gate | executor |
| [verify-profile](engineering/verify-profile/SKILL.md) | Validate opencode.jsonc config integrity (15 checks) | all |
