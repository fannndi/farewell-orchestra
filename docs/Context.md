# Context.md
## Ringkasan
**Current state, cohesion, warnings, background knowledge** untuk sub-proyek farewell-orchestra.

## Workspace Status

- **Timestamp:** 2026-07-28 13:45 UTC
- **Repo:** https://github.com/anomalyco/farewell-orchestra
- **Profile:** Hybrid (2 paid + 2 free)
- **Lokal path:** C:/Users/FANNNDI/Documents/farewell-orchestra
- **Worker type:** foreground-only, deny-by-default

## Active Focus

### Utama
**Maintain orchestrator framework** (agents, skills, commands, templates, config profiles)

### Secondary
- Strengthen linting rules (naming consistency, dead code removal)
- Fix external directory multi-use auth
- Implement portable multi-project cross-access

## Tech Stack

| Komponen | Versi | Status |
|----------|-------|--------|
| OpenCode Core | v2.x | ✅ Build |
| 9Router Gateway | OK | ✅ Ready |
| Zod.js | v4-core | ✅ Support |
| Bun Runtime | 1.1.2 | ✅ Ready |

## Model Matrix

| Agent | Primary Model | Steps |
|-------|---------------|-------|
| Orchestrator | 9router/oc/nemotron-3-ultra-free | 25 |
| Researcher | 9router/oc/nemotron-3-ultra-free | 22 |
| Reviewer | 9router/oc/nemotron-3-ultra-free | 20 |
| Executor | 9router/oc/nemotron-3-ultra-free | 25 |

## Output Format

- `[LEVEL]/file:line - message`
- Max 3 baris per report
- 1500 lines / 38.4KB per output
- Auto-compact with 5000K reservation

## Blockers

1. **Autocompact key mismatch:** 2026-07-27 — `preserve_recent_tokens` vs `keep.tokens` conflict
2. **Permission gap:** 2026-07-27 — Documents folder not in external_directory
3. **Stale reference:** 2026-07-27 — AGENTS.md skill mapping mismatch

## Roadmap

- `/status` real health check
- Auto post-impl verification hook
- External directory config automation
- Linting: dead code removal, naming consistency per language
---