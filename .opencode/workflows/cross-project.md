# Cross-Project Workflow

Complete workflow for handling external projects.

## Workflow Diagram

```
User: "aku mau kerja di project X"
  │
  ▼
┌─────────────────────────────────────────┐
│ 1. PRE-FLIGHT                          │
│ - Permission check                      │
│ - Path validation                       │
│ - Project type detection                │
└─────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────┐
│ 2. DOCS CHECK                          │
│ - Check 5 core docs                     │
│ - Check 2 conditional docs              │
│ - Check sub-project.md                  │
└─────────────────────────────────────────┘
  │
  ├── All docs exist → Skip to Step 4
  │
  └── Docs missing → Step 3
  │
  ▼
┌─────────────────────────────────────────┐
│ 3. DOCS GENERATION                     │
│ - PRD exists? → Generate from PRD       │
│ - No PRD? → Reverse engineering         │
│ - Generate 5 core docs                  │
│ - Generate sub-project.md               │
└─────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────┐
│ 4. TASK DECOMPOSITION                  │
│ - Understand task                       │
│ - Decompose into work packages          │
│ - Assign to agents                      │
└─────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────┐
│ 5. FAN-OUT                             │
│ - Researcher: analyze codebase          │
│ - Reviewer: security + patterns         │
│ - (parallel execution)                  │
└─────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────┐
│ 6. SYNTHESIZE                          │
│ - Combine researcher + reviewer output  │
│ - Verify findings                       │
│ - Create executor brief                 │
└─────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────┐
│ 7. IMPLEMENT                           │
│ - Executor writes code                  │
│ - Verify build/test/lint                │
│ - Report results                        │
└─────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────┐
│ 8. POST-FLIGHT                         │
│ - Update sub-project.md                 │
│ - Update agent memory                   │
│ - Report to Boss                        │
└─────────────────────────────────────────┘
```

## Detailed Steps

### Step 1: Pre-Flight
1. Check `opencode.jsonc` → agent.permission.external_directory
2. If path not listed → add `"C:/Users/FANNNDI/Documents/project/**": "allow"`
3. Verify path exists
4. Detect project type from root files

### Step 2: Docs Check
1. Glob `<project>/docs/*.md`
2. Check 5 core: PRD.md, Architecture.md, Rules.md, Tasks.md, Context.md
3. Check 2 conditional: Schema.md, API_Contract.md
4. Check sub-project.md

### Step 3: Docs Generation
**If PRD exists (>200 lines):**
1. Read PRD → extract tech stack, features, architecture
2. Generate Architecture.md, Rules.md, Tasks.md, Context.md
3. Skip reverse engineering

**If no PRD:**
1. Researcher deep scan (Phase 1-5)
2. Generate all 5 core docs
3. Consistency check

### Step 4: Task Decomposition
1. Understand task from Boss
2. Decompose into work packages
3. Assign to agents (researcher, reviewer, executor)

### Step 5: Fan-Out
1. Dispatch researcher + reviewer in parallel
2. Wait for both to complete
3. Handle errors/permissions

### Step 6: Synthesize
1. Combine researcher + reviewer output
2. Verify findings
3. Create executor brief

### Step 7: Implement
1. Executor writes code
2. Verify build/test/lint
3. Report results

### Step 8: Post-Flight
1. Update sub-project.md
2. Update agent memory
3. Report to Boss

## Error Recovery

| Error | Recovery |
|-------|----------|
| Permission denied | Add path to config, retry |
| Agent timeout | Reduce scope, re-chunk |
| Docs missing | Generate docs, then continue |
| Build fails | Fix errors, retry |
| Test fails | Fix failures, retry |
