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

## Quality Gates

Quality checks sebelum task dianggap selesai. Jalankan setelah review, sebelum mark done.

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

> Deep security check: pakai STRIDE (review skill) — Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation.

### Gate 4: Performance
- [ ] No performance regressions
- [ ] Efficient algorithms
- [ ] Proper caching

### Gate 5: Documentation
- [ ] Code is self-documenting
- [ ] Complex logic explained
- [ ] API documented

### Process

**Before implementation:** review requirements → check existing code → plan implementation.
**During implementation:** write tests first (TDD) → follow coding standards → check security implications.
**After implementation:** run all tests → check code quality → verify security → check performance → update documentation.

## Quality Metrics

| Metric | Target | Check |
|--------|--------|-------|
| Test coverage | >80% | `npm run test:coverage` |
| Lint errors | 0 | `npm run lint` |
| Type errors | 0 | `npm run typecheck` |
| Security issues | 0 | `npm audit` |
| Performance | No regression | Benchmark |

**Project-type aware:** gates di atas untuk Node. Python: `pytest --cov`, `flake8`. Flutter: `flutter test --coverage`, `dart analyze`. Rust: `cargo test`, `cargo clippy`. Go: `go test ./...`, `go vet`. Skip gate kalau tidak applicable + catat alasannya.

## Rules

1. **All gates must pass** — tidak ada yang boleh skip
   **Skip gate kalau tidak applicable** (contoh: Gate Documentation untuk script) + catat "Gate [N] skipped — not applicable: [alasan]".
2. **Automate** — gunakan tools untuk check
3. **Document** — catat hasil check
4. **Review** — review quality setiap task

## Integration

- Executor run quality gates sebelum report
- Orchestrator verify quality gates
- Quality gates hasilnya dicatat di session state

## Cross-Project Quality Gates

### Pre-Implementation Gates

| Gate | Check | Fail Action |
|------|-------|-------------|
| Permission | Path in external_directory? | Add to config |
| Project Type | Detected? | Run detect-project-type.ps1 |
| Docs | Core docs exist? | Generate docs |
| Dependencies | Installed? | Run auto-deps.ps1 |

### Post-Implementation Gates

| Gate | Check | Fail Action |
|------|-------|-------------|
| Build | Build passes? | Fix errors |
| Test | Tests pass? | Fix failures |
| Lint | No lint errors? | Fix issues |
| Files | All files created? | Create missing |

### Project-Type Specific Gates

| Type | Build | Test | Lint |
|------|-------|------|------|
| Flutter | flutter build apk | flutter test | flutter analyze |
| Node.js | npm run build | npm test | npm run lint |
| Python | python -m build | pytest | ruff check . |
| Rust | cargo build | cargo test | cargo clippy |
| Go | go build ./... | go test ./... | golangci-lint run |

### Gate Report Format

```
QUALITY GATES: [PASS/FAIL]
├── Permission:    [PASS/FAIL]
├── Project Type:  [PASS/FAIL]
├── Docs:          [PASS/FAIL]
├── Dependencies:  [PASS/FAIL]
├── Build:         [PASS/FAIL]
├── Test:          [PASS/FAIL]
├── Lint:          [PASS/FAIL]
└── Files:         [PASS/FAIL]

Result: [X/8] gates passed
```
