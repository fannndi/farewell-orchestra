# Cross-Project Checklist

## Pre-Flight (WAJIB sebelum mulai)

- [ ] **Permission check** — target path di external_directory?
- [ ] **Path exists** — project folder ada?
- [ ] **Git status** — ada uncommitted changes? Flag.
- [ ] **Project type** — detect dari root files
- [ ] **Docs check** — 5 core docs ada?

## Permission Fix (kalau belum ada)

```json
// Tambah ke opencode.jsonc → agent.*.permission.external_directory
"C:/Users/FANNNDI/Documents/project/**": "allow"
```

## Project Type Detection

| Files | Type |
|-------|------|
| `pubspec.yaml` | Flutter/Dart |
| `package.json` | Node.js |
| `requirements.txt` / `pyproject.toml` | Python |
| `Cargo.toml` | Rust |
| `go.mod` | Go |

## Docs Generation

### If PRD Exists (>200 lines)
- [ ] Read PRD → extract tech stack, features, architecture
- [ ] Generate Architecture.md from PRD
- [ ] Generate Rules.md from PRD + code patterns
- [ ] Generate Tasks.md from PRD features
- [ ] Generate Context.md from PRD background
- [ ] Verify with code scan (light)

### If No PRD
- [ ] Researcher deep scan (Phase 1-5)
- [ ] Generate all 5 core docs
- [ ] Consistency check

## Post-Generation

- [ ] Run verify-docs.ps1
- [ ] Create sub-project.md
- [ ] Update session memory
- [ ] Report to Boss
