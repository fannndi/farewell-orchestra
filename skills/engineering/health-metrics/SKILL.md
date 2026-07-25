---
name: health-metrics
description: Use at session boundaries or on /status. Tracks orchestrator health: clarity rate, drift rate, rework rate, skill usage. Read-only.
---

## Purpose

Track orchestrator effectiveness per session. Without metrics, you can't improve what you don't measure. Lightweight — no persistent store. Reset each session.

## Trigger

Invoke:
- On `/status` command from Boss
- At end of session (report summary)
- Automatically every 5 tasks (checkpoint)

## Process

1. **Count tasks** — how many requests processed this session?
2. **Clarity rate** — berapa banyak yang perlu `clarify-intent`? (vague prompt %)
3. **Drift rate** — berapa banyak task yang drift-guard flag?
4. **Rework rate** — berapa banyak Boss correction (`salah`/`fix`)?
5. **Skill usage** — skill mana yang paling sering dipanggil?
6. **Cost estimate** — rough token usage this session
7. **Verdict** — 🟢 Healthy / 🟡 Warning / 🔴 Critical

## Output Format

```
📊 Session Health:
   Tasks:     [N] completed
   Clarity:   [X]/[N] perlu clarify ([Y]% jelas)
   Drift:     [X]/[N] drift detected
   Rework:    [X]/[N] rework ([Y]% error)
   Tokens:    ~[N]k est.
   Top Skill: [skill name] ([N]x)
   ─────────────────────────
   Verdict:   🟢 Healthy
```

## Thresholds

| Metric | 🟢 Healthy | 🟡 Warning | 🔴 Critical |
|--------|-----------|-----------|-------------|
| Clarity (need clarify) | ≤30% | 30-60% | >60% |
| Drift (detected) | 0% | 1-20% | >20% |
| Rework (corrections) | ≤20% | 20-40% | >40% |

## Rules

- Reset setiap session baru. Jangan carry-over dari session sebelumnya.
- Report hanya kalau diminta (`/status`) atau checkpoint (setiap 5 task) atau session end.
- 🟡 Warning → brief note apa yang perlu improvement.
- 🔴 Critical → suggest concrete action. "Clarity 70% → pertimbangkan tambah contoh di clarify-intent skill."
- Read-only. Tidak mengubah file apa pun.
- In-memory tracking. Tidak write ke disk.

## Failure Modes

- **Over-reporting** — laporkan setiap task. Bikin noise. Hanya checkpoint & on-demand.
- **Metric obsession** — fokus ke angka, lupa konteks. 1 drift di task kompleks ≠ 1 drift di task trivial.
- **False healthy** — semua 🟢 karena task terlalu mudah. Kalau session cuma 2 task trivial, metrics tidak berarti.
