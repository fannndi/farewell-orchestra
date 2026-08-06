# Changelog

All notable changes to Farewell Orchestra.

## [Unreleased]

### Added
- Auto-load system for skills AND personas (3 layer enforcement)
- progress-tracker skill — persistent task tracking
- error-handler skill — error classification + recovery
- context-manager skill — context prioritization
- Interrupt handler — BLOCKING = escalate langsung
- persona-context-*.md — auto-generated persona files
- skill-context-*.md — auto-generated skill files

### Changed
- AGENTS.md — complete rewrite to reflect current state (13 skills, auto-load system)
- Agent prompts — now reference persona context files
- auto-load-skills.py — now generates persona context

## [2026-08-06]

### Added
- check-consistency.py — automated drift detection (skills, agents, permissions)
- test_integration.py — golden-path integration tests for all profiles
- CHANGELOG.md — this file
- KISS output philosophy — factory vs product
- 4 new KISS skills: kiss-checklist, anti-patterns, simplification, complexity-budget
- Skills per role assignment
- LLM NOTE in README — prevent false-flagging as over-engineered

### Fixed
- test_generate.py — updated imports to match current API
- ci.yaml — updated to expect 13 skills, 5 agents
- generate.py — added all skills to permission allowlist
- verify.py — added evidence tag adjacency checks
- check-links.py — strip code blocks before regex
- post-generate.py — ported PowerShell hook to Python
- verify.py — fixed syntax error (leftover elif)

### Removed
- Orphan dispatch templates (audit.md, fix.md, implement.md, research.md)

### Changed
- Personas enhanced with KISS focus
- README reworked with KISS philosophy

## [2026-08-05]

### Added
- Cross-project workflow
- Reverse engineering mode
- 5+2 docs generation
- Programmatic validation

### Changed
- Simplified personas (identity-driven)
- Simplified skills (purpose + steps + format)
- AGENTS.md streamlined

## [2026-08-04]

### Added
- LLM compatibility protocol
- Fallback mode for all LLMs
- Explicit enforcement rules

### Changed
- Removed "weak LLM" labels
- Renamed "Simplified Mode" to "Fallback Mode"

## [2026-08-03]

### Added
- Proactive & goal-oriented philosophy
- Session memory system
- Lessons integration

### Changed
- Personas redesigned (identity-driven)
- Skills consolidated (11 → 6)

## [2026-08-02]

### Added
- Initial multi-agent system
- 4 agents: orchestrator, researcher, reviewer, executor
- 11 skills (original)
- Profile system with 5 profiles
- Verification gate
- STRIDE audit framework

### Architecture
- Orchestrator → decompose → fan-out → synthesize → executor
- Evidence-first approach (file:line mandatory)
- Freeze Rule (orchestrator never writes code)
- Trust boundary (sub-agents are capable)
