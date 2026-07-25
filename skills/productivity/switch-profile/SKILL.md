---
name: switch-profile
description: Use when switching between Farewell Orchestra profiles. Guided menu: paid, hybrid, free, or free-backup.
disable-model-invocation: true
---

## Purpose

Switch the active opencode profile. Presents the 4 available profiles with their model assignments and cost tier. Restarts opencode with the selected config.

## Process

1. Display the 4 profiles with their model assignments
2. Let Boss pick 1-4
3. Run `opencode -c profiles/opencode.{choice}.jsonc`
4. Confirm active profile

## Profiles Reference

| # | Profile | Orchestrator | Researcher | Reviewer | Executor | Tier |
|---|---------|-------------|------------|----------|----------|------|
| 1 | paid | deepseek-v4-pro | deepseek-v4-flash | deepseek-v4-flash | deepseek-v4-pro | Paid |
| 2 | hybrid | deepseek-v4-flash | north-mini-code-free | deepseek-v4-flash | deepseek-v4-flash | Mixed |
| 3 | free | nemotron-3-ultra-free | north-mini-code-free | nemotron-3-ultra-free | nemotron-3-ultra-free | Free |
| 4 | free-backup | nemotron-3-ultra-550b-free | north-mini-code-free | nemotron-3-ultra-550b-free | nemotron-3-ultra-550b-free | Free (OpenRouter) |

## Commands

```bash
opencode -c profiles/opencode.paid.jsonc        # Profile 1
opencode -c profiles/opencode.hybrid.jsonc      # Profile 2
opencode -c profiles/opencode.free.jsonc        # Profile 3
opencode -c profiles/opencode.free-backup.jsonc  # Profile 4
```

## Rules

- Windows users: double-click `switch.bat` for graphical menu. Equivalent to this skill.
- After switching, run `/status` to verify the new profile loaded correctly.
- Profile switch persists only for current opencode session. Reopen = back to default.
