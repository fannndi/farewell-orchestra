---
name: context-window
description: Optimize context window usage for LLM efficiency.
activation: When context full
trigger: Context >80%
---

# Context Window

Optimalkan penggunaan context window.

## Step-Based Context Estimation

LLM tidak punya token counter — estimasi dari step count:

| Step / max | Estimasi context | Action |
|-----------|-----------------|--------|
| 25% | ~30% | Normal |
| 50% | ~55% | Rencanakan compress |
| 75% | ~80% | Compress: drop Low/Medium, ringkas tool output |
| 90%+ | ~95% | Prioritaskan selesai, hindari baca file besar |

**Decision rule:** 75-80% → compress dulu. Masih >80% setelah compress → handoff. (Compress menang di overlap zone.)

Estimasi ini kasar — kalau ada tool output besar (file read >200 baris), naikkan estimasi 1 level.

**Basis estimasi: 128K floor.** Step table dihitung dari asumsi model terkecil. Model lebih besar (256K/1M) = estimasi ini konservatif — tetap aman.

## Context Priority

| Priority | Context | Keep | Drop |
|----------|---------|------|------|
| 1 (Critical) | Current task, errors | Always | Never |
| 2 (High) | Active files, recent changes | Usually | Only if full |
| 3 (Medium) | Related code, dependencies | Sometimes | If not relevant |
| 4 (Low) | Historical, old sessions | Rarely | Usually |

## Context Format

```markdown
## Context (Priority: [level])

### Critical
- Current task: [deskripsi]
- Blockers: [list]

### High
- Recent decisions: [list]
- Active context: [deskripsi]

### Medium
- Historical: [ringkasan]

### Low
- Old sessions: [ringkasan]
```

## Optimization Rules

### 1. Compress

```markdown
# Before (100 tokens)
The authentication module is located in src/auth.ts. It handles user login, 
registration, and password reset. The module uses JWT tokens for authentication.
The token expiry is set to 24 hours.

# After (30 tokens)
src/auth.ts — auth module (login, register, reset). JWT, 24h expiry.
```

### 2. Deduplicate

```markdown
# Before
- File src/auth.ts handles authentication
- File src/auth.ts uses JWT
- File src/auth.ts has 24h expiry

# After
- src/auth.ts — auth (JWT, 24h expiry)
```

### 3. Summarize

```markdown
# Before (detailed)
1. First, I analyzed the codebase structure
2. Then I identified the authentication module
3. After that, I reviewed the security implications
4. Finally, I implemented the changes

# After (summary)
Analyzed → identified auth module → reviewed security → implemented
```

### 4. Prioritize

Kalau context penuh:
1. Drop Low priority dulu
2. Then Medium priority
3. Keep High and Critical

### 5. Reload (Context Empty)

Kalau context kosong:
1. Load Critical dari sub-project.md
2. Load High dari recent memory
3. Load Medium dari lessons
4. Skip Low

## Context Budget

| Agent | Budget | Strategy |
|-------|--------|----------|
| Orchestrator | 8K tokens | Focus on task + decisions |
| Researcher | 4K tokens | Focus on findings + evidence |
| Reviewer | 4K tokens | Focus on issues + impact |
| Executor | 6K tokens | Focus on code + verification |

## Rules

1. **Compress** — kurangi token tanpa hilang makna
2. **Deduplicate** — hapus duplikasi
3. **Summarize** — ringkas detail
4. **Prioritize** — drop yang kurang penting
5. **Budget** — patuhi budget per agent
6. **Update** — refresh context setiap step

## Integration

- Context manager gunakan skill ini
- Orchestrator compress context sebelum dispatch
- Sub-agents dapat context sesuai budget

## Cross-Project Context Management

### Context Priority
When working on cross-project tasks:

1. **Project info** — path, type, tech stack (always keep)
2. **Current task** — what is being worked on (always keep)
3. **Agent status** — what each agent is doing (keep latest)
4. **File contents** — only keep relevant files (prune old)
5. **Error messages** — keep until resolved, then prune

### Context Compression Strategy

| Context Type | Keep | Prune |
|--------------|------|-------|
| Project path | Always | Never |
| Current task | Always | Never |
| Agent status | Latest only | Old status |
| File contents | Relevant only | Old files |
| Error messages | Until resolved | After fix |
| Debug output | Never | Always |

### Cross-Project Context Switch

When switching between projects:
1. Save current project context to sub-project.md
2. Load new project context from sub-project.md
3. Clear old file contents from context
4. Keep: project path, task, agent status

### Context Window Size Estimation

| Content Type | Size (tokens) |
|--------------|---------------|
| Project path | ~10 |
| Task description | ~50-100 |
| Agent status (1) | ~20 |
| File content (100 lines) | ~500 |
| Error message | ~50-100 |
| Full codebase (26 files) | ~15000 |

### Auto-Prune Rules

1. File contents > 1000 lines → summarize
2. Error messages > 5 → keep latest 3
3. Agent status > 3 → keep latest
4. Debug output → always prune
