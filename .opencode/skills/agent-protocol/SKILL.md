---
name: agent-protocol
description: Communication standard between agents.
activation: When agents communicate
trigger: Agent dispatch
---

# Agent Protocol

Standard komunikasi antar agents.

## Message Format

### Orchestrator → Sub-agent

```json
{
  "task": "apa yang harus dilakukan",
  "files": ["file1.ts", "file2.ts"],
  "context": "kenapa, constraint",
  "format": "expected output format",
  "verify": "how to verify"
}
```

### Sub-agent → Orchestrator

```json
{
  "status": "DONE/BLOCKED/FAILED",
  "output": "hasil kerja",
  "files_changed": ["file1.ts"],
  "issues": ["issue1", "issue2"],
  "next": "apa yang perlu dilakukan selanjutnya"
}
```

### Error Response

```json
{
  "status": "FAILED",
  "error": "apa yang salah",
  "type": "RETRY/FALLBACK/ESCALATE/SKIP/ABORT",
  "suggestion": "bagaimana cara fix"
}
```

## Communication Rules

1. **Structured** — gunakan format yang sudah didefinisikan
2. **Concise** — jangan basa-basi
3. **Actionable** — selalu ada next step
4. **Evidence-based** — sertakan file:line untuk claims

## Interrupt Protocol

Kalau ada BLOCKING:
```json
{
  "interrupt": true,
  "type": "BLOCKING",
  "message": "apa yang salah",
  "file": "file:line",
  "action": "apa yang harus dilakukan"
}
```

## Context Passing

```json
{
  "context": {
    "session_state": "apa yang sedang dikerjakan",
    "decisions": ["decision1", "decision2"],
    "blockers": ["blocker1"],
    "files_modified": ["file1.ts"]
  }
}
```

## Rules

1. **Structured** — gunakan format yang sudah didefinisikan
2. **Concise** — jangan basa-basi
3. **Actionable** — selalu ada next step
4. **Evidence-based** — sertakan file:line untuk claims
5. **Interrupt-aware** — BLOCKING = escalate langsung
