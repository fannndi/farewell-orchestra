# Session State — Cross-Project

## State Tracking

When working on cross-project tasks, track:

```markdown
## Session State

### Project Info
- **Path:** [absolute path]
- **Type:** [Flutter/Node/Python/Rust/Go]
- **Permission:** [configured/not configured]

### Progress
- [ ] Pre-flight (permission, path, type)
- [ ] Docs check
- [ ] Docs generation (if needed)
- [ ] Task decomposition
- [ ] Implementation
- [ ] Verification

### Agent Status
- Researcher: [idle/running/done/error]
- Reviewer: [idle/running/done/error]
- Executor: [idle/running/done/error]

### Context
- Last action: [what was done]
- Current focus: [what is being worked on]
- Blockers: [any issues]
```

## State Transitions

```
IDLE → PRE_FLIGHT → DOCS_CHECK → [DOCS_GEN] → DECOMPOSE → IMPLEMENT → VERIFY → DONE
                                      ↑
                                      └── if docs missing
```

## Error States

| State | Cause | Recovery |
|-------|-------|----------|
| PERMISSION_DENIED | Path not in whitelist | Add to config, retry |
| AGENT_TIMEOUT | Task too large | Reduce scope, re-chunk |
| AGENT_ERROR | Sub-agent failed | Retry once, then escalate |
| DOCS_INCOMPLETE | Missing core docs | Generate docs, then continue |
