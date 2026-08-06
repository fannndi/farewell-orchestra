# Changelog

All notable changes to Farewell Orchestra.

## [Unreleased]

### Added
- check-consistency.py — automated drift detection (skills, agents, permissions)
- test_integration.py — golden-path integration tests for all profiles
- CHANGELOG.md — this file

### Fixed
- test_generate.py — updated imports to match current API (removed collect_models, short_model_id, BOILERPLATE, rollback)
- ci.yaml — updated to expect 10 skills, 5 agents (including boss.md)
- generate.py — added 4 new skills to permission allowlist (kiss-checklist, anti-patterns, simplification, complexity-budget)
- verify.py — added evidence tag [P/W/E/O] adjacency check
- check-links.py — strip code blocks before regex to avoid false positives
- post-generate.py — ported PowerShell hook to Python for cross-platform

### Removed
- Orphan dispatch templates (audit.md, fix.md, implement.md, research.md)

## [2026-08-06]

### Added
- KISS output philosophy — factory vs product
- 4 new KISS skills: kiss-checklist, anti-patterns, simplification, complexity-budget
- Skills per role assignment
- LLM NOTE in README — prevent false-flagging as over-engineered

### Changed
- Personas enhanced with KISS focus
- README reworked with KISS philosophy

## [2026-08-05]

### Added
- Cross-project workflow
- Reverse engineering mode
- 5+2 docs generation
- Programmatic validation (validate_output.py)

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
