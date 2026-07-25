---
name: clarify-intent
description: Use when Boss prompt is vague or ambiguous. Forces structured clarification before any execution. Always invoked pre-flight.
---

## Purpose

Prevent garbage-in-garbage-out. When Boss gives vague instructions, this skill forces 2-3 concrete options before anything executes. Boss picks one → execution proceeds. No guessing, no assuming.

## Trigger

Invoke AUTOMATICALLY when:
- Boss request has no explicit file/folder scope
- Boss uses vague verbs: "perbaikin", "tambahin", "benerin", "rapihin", "optimasi"
- Acceptance criteria not stated and not obvious
- Multiple interpretations possible
- Request is under 10 words total
- Orchestrator's pre-flight checklist flags ambiguity

## Process

1. **Extract what IS known** — any explicit files, functions, constraints. State them first.
2. **Identify the gap** — what's missing? Scope? Acceptance? Goal?
3. **Generate 2-3 concrete options** — masing-masing 1 kalimat, actionable, mutually exclusive
4. **Recommend 1** (optional) — with "(Recommended)" suffix, 1-line reason
5. **Boss picks** → proceed to orchestrator dispatch

## Output Format

```
Yang jelas: [apa yang sudah diketahui]

Maksudnya:
1. [Opsi A] — [1 kalimat]
2. [Opsi B] — [1 kalimat] (Recommended)
3. [Opsi C] — [1 kalimat]

Pilih 1/2/3?
```

## Rules

- Max 3 options. Kalau perlu >3 → problemnya terlalu besar, pecah dulu.
- Setiap opsi harus MUTUALLY EXCLUSIVE. Boss tidak boleh bisa pilih dua.
- Jangan tanya "maksudnya apa?" tanpa opsi. Itu buang token.
- Kalau benar-benar tidak ada yang jelas → 1 opsi: "Coba jelaskan ulang goal-nya dalam 1 kalimat"
- Setelah Boss pilih → LANGSUNG ke orchestrator untuk dispatch. Jangan klarifikasi lagi.
- Jangan pernah execute sendiri. Hanya klarifikasi, lalu serahkan ke orchestrator.

## Failure Modes

- **Over-clarifying** — Boss udah jelas ("ganti `>` jadi `>=` di auth.ts:42") tapi tetap tanya opsi. Jangan.
- **Under-clarifying** — Boss bilang "fix auth" dan langsung dispatch ke researcher. Hentikan.
- **Option paralysis** — kasih 5+ opsi. Boss overwhelm. Max 3.
- **Leading options** — semua opsi mengarah ke solusi yang sama. Harus genuinely berbeda.
- **Clarify loop** — Boss pilih, lalu klarifikasi lagi. Sekali cukup.
