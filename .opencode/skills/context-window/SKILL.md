---
name: context-window
description: Optimize context window usage for LLM efficiency.
---

# Context Window

Optimalkan penggunaan context window.

## Context Priority

| Priority | Context | Keep | Drop |
|----------|---------|------|------|
| 1 (Critical) | Current task, errors | Always | Never |
| 2 (High) | Active files, recent changes | Usually | Only if full |
| 3 (Medium) | Related code, dependencies | Sometimes | If not relevant |
| 4 (Low) | Historical, old sessions | Rarely | Usually |

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

## Integration

- Context manager gunakan skill ini
- Orchestrator compress context sebelum dispatch
- Sub-agents dapat context sesuai budget
