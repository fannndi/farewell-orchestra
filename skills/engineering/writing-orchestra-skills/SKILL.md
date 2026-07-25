---
name: writing-orchestra-skills
description: Use when creating, editing, or reviewing Farewell Orchestra skills. The meta-skill for skill authorship.
disable-model-invocation: true
---

## Purpose

How to write skills for Farewell Orchestra. Follow these rules when creating new skills or improving existing ones.

## Skill Anatomy

Every SKILL.md must have:
```yaml
---
name: <kebab-case-name>
description: <one-line trigger — when to use this skill>
# omit for model-invoked; add for user-invoked:
disable-model-invocation: true
# optional:
argument-hint: "<what args to pass>"
---
```

## Sections

Every SKILL.md must have these sections:
1. `## Purpose` — what this skill does, in 1-2 sentences
2. `## Trigger` — when to invoke (or `## When To Fire` for user-invoked)
3. `## Process` — numbered steps. Each step ends with a **checkable completion criterion**
4. `## Rules` — bullet list of constraints
5. `## Failure Modes` — what goes wrong when this skill is misused

## Invocation Rules

| Type | Frontmatter | Context Load | Discoverable By |
|------|-------------|-------------|-----------------|
| Model-invoked | No `disable-model-invocation` | Yes (description in context) | Agent auto-discovers |
| User-invoked | `disable-model-invocation: true` | Zero (only name) | Human must remember |

## Quality Gates

- **No-op test**: every line must change behavior vs default. Delete lines that don't.
- **Completion criterion**: every step ends with something checkable. "Research the codebase" → FAIL. "Research the codebase and return ≥3 file:line findings" → PASS.
- **Negation is failure**: prompt what TO do, not what NOT to do. "Don't use grep" → FAIL. "Use codebase-memory search_graph" → PASS.
- **Leading words over explanation**: use terms the model already knows. "Fog of war", "tracer bullet", "frontier".
- **Progressive disclosure**: inline what every branch needs. Push behind pointer what only some branches reach.
- **Single source of truth**: every concept in exactly ONE skill. Cross-reference, don't duplicate.

## When to Split a Skill

Split when:
- Different invocation mode (user vs model)
- Different agent role (orchestrator vs executor)
- Post-completion steps diverge significantly
- Skill exceeds ~80 lines

Don't split when:
- It's one workflow with natural sequence
- All branches share the same completion criterion
- Splitting would create a "remember to run X after Y" cognitive burden
