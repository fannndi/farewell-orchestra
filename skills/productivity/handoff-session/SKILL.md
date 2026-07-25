---
name: handoff-session
description: Use when ending a session but work is unfinished. Saves current state — active profile, TODO list, last task, open questions — so the next session can resume seamlessly.
disable-model-invocation: true
argument-hint: "What should the next session focus on?"
---

## Purpose

Save session state for seamless cross-session resume. Boss shouldn't need to re-explain context. This skill creates a handoff file that the next session reads on startup.

## When To Fire

- Boss says "lanjut besok" or "stop dulu" or "nanti aja"
- Context window is near full and you need to compact
- Work is incomplete but session needs to end

## Process

1. Capture current state: active profile, current TODO list, last completed step, next pending step
2. Capture open questions: what's still ambiguous, what needs Boss decision
3. Capture context: which files were touched, which skills are loaded
4. Write handoff to `.farewell/handoffs/handoff-YYYYMMDD-HHMM.md`
5. Report: "Handoff saved. Next session: say 'resume' to continue."

## Handoff Template

```markdown
# Handoff — YYYY-MM-DD HH:MM

## Profile
{active profile name}

## Status
- Last completed: {step}
- Next pending: {step}
- TODO remaining: {count} items

## Open Questions
- {question 1}
- {question 2}

## Context
- Files touched: {list}
- Skills loaded: {list}
- Active model: {model name}

## Resume Instructions
Say "resume" or "lanjutin" to continue from where we left off.
```

## Rules

- Save to `.farewell/handoffs/` — create directory if it doesn't exist
- Never include secrets, API keys, or sensitive data in handoff
- Reference files by path, never duplicate content
- Next session: orchestrator reads latest handoff automatically on `/start`

## Failure Modes

- **No handoff** — ending a session with unfinished work and no state saved. Next session starts blind.
- **Secrets in handoff** — copying API keys, tokens, or passwords into the handoff file. Never.
- **Content duplication** — pasting entire files into the handoff. Reference by path only. Drives token waste on resume.
