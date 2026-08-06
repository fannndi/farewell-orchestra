# Project Management Guide

Guide for managing multiple projects with Farewell Orchestra.

## Project Lifecycle

### 1. Discovery
- User mentions project path
- Detect project type
- Check docs status

### 2. Onboarding
- Generate docs (if missing)
- Create sub-project.md
- Setup permissions

### 3. Active Work
- Decompose tasks
- Fan-out to agents
- Implement changes
- Verify results

### 4. Completion
- Update docs
- Update sub-project.md
- Report to Boss

## Project Registry

Track all projects in sub-project.md files:

| Project | Path | Type | Status | Last Active |
|---------|------|------|--------|-------------|
| git-watcher | C:/Users/FANNNDI/Documents/git-watcher | Flutter | Active | 2026-08-06 |
| farewell-orchestra | C:/Users/FANNNDI/Documents/farewell-orchestra | Config | Active | 2026-08-06 |

## Multi-Project Workflow

### Switching Projects
1. Save current project context to sub-project.md
2. Load new project context from sub-project.md
3. Clear old file contents from context
4. Continue work on new project

### Parallel Projects
- Use different agent instances for each project
- Track progress separately
- Report status per project

## Project Health Monitoring

Run periodically:
```powershell
.\scripts\project-health.ps1 -ProjectPath "C:\path\to\project"
.\scripts\project-dashboard.ps1 -ProjectPath "C:\path\to\project"
```

## Documentation Standards

### Required per Project
- sub-project.md — project overview + agent memory
- docs/ — 5 core docs + conditional docs

### Recommended
- README.md — project description
- CHANGELOG.md — change history
- .gitignore — version control
