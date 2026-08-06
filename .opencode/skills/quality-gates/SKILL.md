---
name: quality-gates
description: Quality checks before marking task as done.
activation: Before reporting done
trigger: Executor selesai
---

# Quality Gates

Quality checks sebelum task dianggap selesai.

## Gates

### Gate 1: Functionality
- [ ] Code works as expected
- [ ] All tests pass
- [ ] No regressions

### Gate 2: Code Quality
- [ ] Follows coding standards
- [ ] No code smells
- [ ] Proper naming

### Gate 3: Security
- [ ] No security vulnerabilities
- [ ] Input validation
- [ ] Authentication/authorization

### Gate 4: Performance
- [ ] No performance regressions
- [ ] Efficient algorithms
- [ ] Proper caching

### Gate 5: Documentation
- [ ] Code is self-documenting
- [ ] Complex logic explained
- [ ] API documented

## Process

### Before Implementation
1. Review requirements
2. Check existing code
3. Plan implementation

### During Implementation
1. Write tests first (TDD)
2. Follow coding standards
3. Check security implications

### After Implementation
1. Run all tests
2. Check code quality
3. Verify security
4. Check performance
5. Update documentation

## Quality Metrics

| Metric | Target | Check |
|--------|--------|-------|
| Test coverage | >80% | `npm run test:coverage` |
| Lint errors | 0 | `npm run lint` |
| Type errors | 0 | `npm run typecheck` |
| Security issues | 0 | `npm audit` |
| Performance | No regression | Benchmark |

## Rules

1. **All gates must pass** — tidak ada yang boleh skip
2. **Automate** — gunakan tools untuk check
3. **Document** — catat hasil check
4. **Review** — review quality setiap task

## Integration

- Executor run quality gates sebelum report
- Orchestrator verify quality gates
- Quality gates hasilnya dicatat di session state

## Contoh

```markdown
## Quality Gates: Tambahin fitur login

### Gate 1: Functionality ✅
- [x] Login endpoint works
- [x] JWT token generated
- [x] Invalid password rejected

### Gate 2: Code Quality ✅
- [x] Follows naming conventions
- [x] No code smells
- [x] Proper error handling

### Gate 3: Security ✅
- [x] Password hashed
- [x] JWT signed
- [x] Rate limiting added

### Gate 4: Performance ✅
- [x] Login < 100ms
- [x] No N+1 queries

### Gate 5: Documentation ✅
- [x] API documented
- [x] Error codes documented
```
