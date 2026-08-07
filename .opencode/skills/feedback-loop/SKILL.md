---
name: feedback-loop
description: Record, verify, learn from task results. Automatic improvement.
activation: After task complete
trigger: Task selesai
---

# Feedback Loop

Record → Verify → Learn → Apply

## When to Call learn()

| Trigger | Call learn? |
|---------|-------------|
| Task SUCCESS with issue discovered | YES |
| Task FAILURE | YES |
| Task PARTIAL | YES |
| Pattern repeats 3x | YES |
| Orchestrator corrects agent | YES |
| Task SUCCESS, no issues | NO |

## Process

### 1. Record (After Each Task)

Orchestrator mencatat lesson via learn() operation — APPEND manual ke Farewell-Knowlage/Lessons.md (learn adalah tool nyata; bukan pseudo-code).

Format append ke Lessons.md:
| date | trigger | error | root cause | fix | rule_updated | pattern_count |

**Example:**
```
learn(trigger="implement login feature", error="rate limiter too complex", root_cause="added unnecessary abstraction layer", fix="simplified to 3-line middleware", verification="npm test", verified="pass")
```

### 2. Verify (During Task)

Before marking done:
- Check if action matches existing rules
- Check if error matches known patterns in Lessons.md (external vault)
- Flag if pattern repeats

### 3. Learn (End of Session)

Orchestrator reviews:
- Read Lessons.md (external vault)
- Identify patterns (errors 3+ times)
- Suggest rule updates to AGENTS.md or Rules.md

### 4. Apply (Start of Session)

Before new task:
- Read Lessons.md (external vault)
- Check for patterns matching current task type
- Apply relevant rules automatically

## Rules

1. **Always record failures** — no exceptions
2. **Record issues even on success** — if something went wrong but task succeeded, still log
3. **Skip only clean success** — task SUCCESS with zero issues = skip learn call
4. **Pattern threshold = 3** — after 3x same error, create rule
5. **One learn call per task** — don't spam, summarize all issues in one call

## Output

After learn call, orchestrator reports:
```
[FEEDBACK] logged to Lessons.md (external vault)
[PATTERN] (if applicable) "X happened 3+ times, rule suggested"
```

## Performance Metrics

Track performa agent dan identifikasi improvement.

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

### Tracking Format

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

### Analysis

- Task type apa yang sering gagal?
- Agent mana yang paling lambat?
- Error type apa yang paling sering?
- Skill yang perlu diupdate
- Rules yang perlu ditambah
- Process yang perlu dioptimasi

### Integration

- Orchestrator track performa setiap task
- Performa dicatat di session state
- Analysis dilakukan setiap 10 tasks

### Cross-Project Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Success rate | >90% | Tasks completed / tasks attempted |
| Avg time | <5min | Time from dispatch to completion |
| Error rate | <10% | Errors / total tasks |
| Permission issues | <5% | Permission errors / total tasks |

### Agent Health Check (sebelum dispatch)

1. Check agent is alive (ping)
2. Check agent has correct permissions
3. Check agent has required skills loaded
4. Check context window is not full

### Performance Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| Slow response | >5min timeout | Reduce scope, re-chunk |
| High error rate | >20% errors | Check prompts, add examples |
| Permission errors | Frequent blocks | Update external_directory |
| Context overflow | Agent crashes | Prune context, compress |

### Agent Improvement Log

```
[date] — [agent] — [improvement] — [result]
```

Example:
```
2026-08-06 — researcher — Added permission pre-check — 0 permission errors
2026-08-06 — reviewer — Added file access patterns — Faster reviews
2026-08-06 — executor — Added Flutter commands — Can test Flutter projects
```
