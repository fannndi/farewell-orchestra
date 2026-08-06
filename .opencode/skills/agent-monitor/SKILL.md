---
name: agent-monitor
description: Track agent performance and identify improvements.
---

# Agent Monitor

Track performa agent dan identifikasi improvement.

## Metrics

### Per Agent
- **Tasks completed** — berapa banyak task selesai
- **Success rate** — persentase task berhasil
- **Average time** — rata-rata waktu per task
- **Error rate** — persentase task gagal

### Per Task Type
- **Feature** — waktu dan success rate untuk fitur baru
- **Bug fix** — waktu dan success rate untuk fix bug
- **Refactor** — waktu dan success rate untuk refactor
- **Research** — waktu dan success rate untuk research

## Tracking Format

```markdown
# Agent Performance

## Orchestrator
- Tasks: 10
- Success: 9 (90%)
- Avg time: 5 min
- Errors: 1 (timeout)

## Researcher
- Tasks: 15
- Success: 14 (93%)
- Avg time: 3 min
- Errors: 1 (not found)

## Reviewer
- Tasks: 12
- Success: 12 (100%)
- Avg time: 2 min
- Errors: 0

## Executor
- Tasks: 20
- Success: 18 (90%)
- Avg time: 10 min
- Errors: 2 (test fail)
```

## Analysis

### Identify Patterns
- Task type apa yang sering gagal?
- Agent mana yang paling lambat?
- Error type apa yang paling sering?

### Identify Improvements
- Skill yang perlu diupdate
- Rules yang perlu ditambah
- Process yang perlu dioptimasi

## Rules

1. **Track** — catat setiap task
2. **Analyze** — cari pattern
3. **Improve** — update berdasarkan analysis
4. **Report** — lapor ke Boss kalau ada issue

## Integration

- Orchestrator track performa setiap task
- Performa dicatat di session state
- Analysis dilakukan setiap 10 tasks

## Contoh

```markdown
# Performance Report

## Summary
- Total tasks: 57
- Success rate: 91%
- Avg time: 5 min

## Top Issues
1. Executor: 2 test failures → need better TDD
2. Researcher: 1 not found → need better search

## Recommendations
1. Add TDD skill untuk executor
2. Improve search strategy untuk researcher
```
