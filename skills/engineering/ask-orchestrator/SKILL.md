---
name: ask-orchestrator
description: Use when Boss needs to understand what skills are available. Maps all Farewell Orchestra skills and how they chain together. Zero context load — just the map, not the territory.
disable-model-invocation: true
---

## Purpose

Router skill. Maps every Farewell Orchestra skill and their relationships. You read this to understand what skills exist and how they chain — you never fire them from here.

## Main Flow (idea → ship)

```
Boss request
  └── /orchestrate (decompose + fan-out)
        ├── /research-codebase (forensic evidence)
        └── /audit-security (STRIDE review)
              └── synthesize
                    └── /implement-change (YAGNI + DoD)
                          └── /verify-profile (post-implementation gate)
```

## Quick Actions (no fan-out needed)

```
Boss says "review X"     → /audit-security directly
Boss says "how does X work?" → /research-codebase directly
Boss says "fix X"        → /implement-change directly
Boss says "test profiles" → /stress-test (full suite)
Boss says "switch profile" → /switch-profile (guided)
```

## Skill Index

| Skill | Role | Invocation | Purpose |
|-------|------|------------|---------|
| orchestrate | orchestrator | model | Decompose → fan-out → synthesize → delegate |
| research-codebase | researcher | model | Forensic investigation, file:line evidence |
| audit-security | reviewer | model | STRIDE audit, 10-domain checklists |
| implement-change | executor | model | YAGNI Ladder, DoD gate |
| verify-profile | all | model | 15-check config validation |
| switch-profile | orchestrator | model | Guided 4-profile switching |
| stress-test | orchestrator | model | 6-test stress suite |
| ask-orchestrator | user | user | This skill — the map |
| grill-boss | user | user | Clarify ambiguous requests |
| full-cycle | orchestrator | model | Complete pipeline in one flow |
| handoff-session | orchestrator | user | Cross-session state bridge |
| compound-review | reviewer | model | Multi-axis parallel review |
| setup-orchestra | orchestrator | user | One-shot setup validation |
| writing-orchestra-skills | user | user | Meta-skill for skill authorship |
