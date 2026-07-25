---
name: implement-change
description: Use when implementing code changes, fixing bugs, or adding features. YAGNI-driven minimal implementation with DoD gate.
---

## Purpose

Implement scoped code changes with minimal diff. Boss pays per token AND per tool call — be stingy. Follow YAGNI Ladder: delete before add, reuse before create. Every change passes the DoD checklist before reporting.

## Trigger

Invoke this skill when:
- Orchestrator delegates an implementation task
- Boss says "fix X" or "implement Y"
- A specific file needs modification per a brief

## Process

1. **Read minimal** — only the files listed in the brief. Don't explore for context.
2. **Plan minimal** — what's the smallest change that satisfies the criteria?
3. **Implement** — follow YAGNI Ladder. Delete over add. Boring over clever.
4. **Verify** — run the EXACT command in the brief. Don't add extra checks.
5. **DoD gate** — pass the Definition of Done checklist before reporting.
6. **Report** — files changed (1 line), verification (1 line), summary.

## YAGNI Ladder

1. Does this need to exist? → No? Stop. Delete.
2. Stdlib does it? → Use it.
3. Platform covers it? → CSS over JS. DB constraint over app code.
4. Existing dependency solves it? → Use it. NEVER add new dep.
5. One line? → One line.
6. Then: minimum code that works.

## Not-Lazy Guard

Never simplify away: input validation at trust boundaries, error handling preventing data loss, security, accessibility, anything Boss explicitly requested.
Non-trivial logic → ONE runnable check (1 assert/unit test). Trivial one-liner → no test.

## Precision Standard

- Typo = 1 character off → reject. Diff-check every identifier.
- Duplication >2x → extract. DRY.
- No premature abstraction: no interface with 1 impl, no factory for 1 product.
- Follow existing file style. Don't mix snake_case/camelCase.
- Output: code first. Then max 3 lines: what skipped, when to add later.

## DoD — Definition of Done

- [ ] Verification passes (per brief command)
- [ ] Zero broken references
- [ ] No TODO/FIXME introduced
- [ ] Diff matches scope — no extra files touched
- [ ] Naming consistent with file edited
- [ ] Lint clean

## Cleanup

Before reporting, always:
- Delete unused imports, dead variables, dead comments
- Remove console.log, breakpoints, debug prints
- Check naming consistency with the file edited

## Rules

- Read files ONLY if needed. Brief tells you file+line → go straight there.
- Prefer delete over add. 5 lines deleted > 3 added.
- One change per edit. Don't batch unrelated fixes.
- Don't delegate. You're the terminal node.
- Don't widen scope. Mention out-of-scope issues, don't fix them.
- Don't fake test results. Can't run test → say why.
- If clean: "Done. X file(s) changed. Test passes." — that's it.

## Chaining

After implementation, this skill triggers:
- `verify-profile` — if config files were touched
- `compound-review` — if change was >50 lines (self-review gate)

If multiple implementations are needed, consider `full-cycle` which orchestrates the complete pipeline.

## Failure Modes

- **Over-reading** — reading 5 files when brief said "edit line 42 of auth.ts". Waste tokens.
- **Over-engineering** — extracting a utility when one inline function would do. YAGNI.
- **Silent scope creep** — fixing a nearby "obvious bug" without permission. Mention it, don't fix it.
- **Missing DoD** — reporting "done" without running verification. Gate yourself.
