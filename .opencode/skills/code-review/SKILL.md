---
name: code-review
description: Two-axis review: Standards + Spec. Parallel sub-agents.
activation: When reviewing PR
trigger: PR/branch exists
---

# Code Review

Two-axis review:
1. **Standards** — apakah kode ikut coding standards?
2. **Spec** — apakah kode sesuai dengan spec/issue?

## Process

### 1. Tentukan Fixed Point

```bash
git diff <fixed-point>...HEAD
git log <fixed-point>..HEAD --oneline
```

Fixed point: commit SHA, branch, tag, atau `main`.

### 2. Identify Spec Source

1. Issue references di commit messages
2. Path yang user berikan
3. Spec file di `docs/` atau `specs/`
4. Kalau tidak ada → tanya user

### 3. Identify Standards Sources

- `CODING_STANDARDS.md`
- `CONTRIBUTING.md`
- `Rules.md`
- Existing code patterns

### 4. Parallel Review

Dispatch **researcher** dan **reviewer** parallel:

**Researcher (Standards):**
```
Review diff untuk coding standards:
- Naming conventions
- Code style
- Error handling
- Anti-patterns
```

**Reviewer (Spec):**
```
Review diff untuk spec compliance:
- Requirements yang missing
- Scope creep
- Implementation yang salah
```

### 5. Aggregate

```markdown
## Standards
[findings dari researcher]

## Spec
[findings dari reviewer]

## Summary
- Standards: X findings
- Spec: Y findings
```

## Anti-Patterns

- ❌ Gabungkan Standards dan Spec dalam satu review
- ❌ Skip fixed point validation
- ❌ Review tanpa spec reference
