# Changelog

## 2026-08-06 — Cross-Project Support

### Added
- Permission pre-check for cross-project access
- Project type detection (Flutter, Node.js, Python, Rust, Go)
- Orchestrator direct scan fallback
- Flutter project template (architecture + docs)
- Node.js project template
- Python project template
- Rust project template
- Go project template
- Cross-project checklist
- Automation scripts:
  - verify-docs.ps1 — docs completeness check
  - project-health.ps1 — health score
  - project-dashboard.ps1 — project overview
  - generate-sub-project.ps1 — auto-generate sub-project.md
  - detect-project-type.ps1 — project type detection
  - auto-deps.ps1 — auto-install dependencies
  - auto-test.ps1 — auto-run tests
- Lesson learned: git-watcher experience

### Improved
- Cross-project guide (pre-flight, type detection, fallback)
- Prepare skill (permission pre-check, type detection, PRD flow)
- Orchestrate skill (cross-project orchestration, error recovery)
- Review skill (permission handling, file access patterns)
- Implement skill (project-specific commands, error recovery)
- Handoff skill (cross-project context, session memory)
- Bootstrap-project skill (PRD-heavy mode, permission handling)
- Context-window skill (cross-project context management)
- Error-handler skill (cross-project error patterns)
- Code-review skill (quality gates merged)
- AGENTS.md (cross-project patterns, agent brief format)
- README.md (cross-project support, automation scripts)

### Fixed
- Permission issue — added C:/Users/FANNNDI/Documents/** to all agent external_directory
- Sub-agent access — orchestrator direct scan as fallback
