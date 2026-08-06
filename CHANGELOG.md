# Changelog

All notable changes to Farewell Orchestra.

## [Unreleased]

### Added
- 8 new LLM-centric skills: session-state, task-decomposer, agent-protocol, feedback-loop, context-window, task-priority, quality-gates, agent-monitor
- soul.md — project identity (bukan persona agent)
- Cross-project workflow with reverse engineering

### Removed
- templates/ folder (redundant with cross-project/)

## [2026-08-06]

### Added
- 5 skills from mattpocock/skills synthesis: tdd, code-review, diagnose-bugs, handoff, domain-modeling
- Auto-load system for skills AND personas (3 layer enforcement)
- 4 KISS skills: kiss-checklist, anti-patterns, simplification, complexity-budget
- 3 management skills: progress-tracker, error-handler, context-manager
- Interrupt handler (BLOCKING = escalate langsung)
- LLM NOTE in README
- check-consistency.py — automated drift detection
- test_integration.py — golden-path integration tests
- CHANGELOG.md

### Fixed
- test_generate.py — updated imports
- ci.yaml — updated to 26 skills, 5 agents
- generate.py — all skills in permission allowlist
- verify.py — evidence tag adjacency checks
- check-links.py — strip code blocks
- post-generate.py — ported to Python
- switch.bat — interactive menu with dynamic profiles

### Removed
- Orphan dispatch templates
- Windows-only scripts (except switch.bat)
- .codenomad/ leftover
- Stress test documentation files

## [2026-08-05]

### Added
- Cross-project workflow
- Reverse engineering mode
- 5+2 docs generation
- Programmatic validation

### Changed
- Simplified personas (identity-driven)
- Simplified skills (purpose + steps + format)

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
