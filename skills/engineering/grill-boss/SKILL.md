---
name: grill-boss
description: Use when Boss's request is ambiguous and needs clarification before dispatching. Asks ONE precise question at a time. Never guesses.
disable-model-invocation: true
---

## Purpose

Clarify ambiguous requests before dispatch. Boss pays per token — a wrong dispatch costs more than a clarifying question. Ask ONE question at a time. Multiple questions = bewildering.

## When To Fire

Boss says something and you're not 90% sure what they mean. Examples:
- "bikin yg bagus" — what does "bagus" mean here?
- "fix auth" — which auth? Login? Token? Middleware?
- "optimize" — speed? Memory? Bundle size? DB queries?

## Process

1. Identify the ONE most critical ambiguity
2. Ask it in ≤1 sentence. Offer 2-3 concrete options.
3. Boss answers → you now have clarity. Dispatch.
4. Boss answers but new ambiguity emerges → ask ONE more question.
5. Max 3 rounds. After 3 → pick the most likely interpretation and go. Report your assumption.

## Rules

- NEVER ask "what do you mean?" without offering concrete options. That's lazy.
- NEVER ask multiple questions in one message. One at a time.
- NEVER apologize for asking. Clarity is cheaper than wrong code.
- After clarity: dispatch immediately. Don't re-summarize what Boss just said.
- If Boss says "terserah" or "you decide" → pick, go, report assumption. Don't ask again.

## Failure Modes

- **Optionless question** — "what do you mean by that?" without options. Force the Boss to do your thinking.
- **Question barrage** — 3+ questions in one message. Overwhelming. Pick the ONE most important.
- **Endless clarification** — 4+ rounds of questions. After 3 rounds, just pick and go.
- **Re-summarizing** — Boss clarifies, you repeat it back. Just dispatch. Tokens wasted.
