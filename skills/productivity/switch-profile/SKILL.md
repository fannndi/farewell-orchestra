---
name: switch-profile
description: Use when Boss wants to switch between profiles. Orchestrator CANNOT restart opencode (bash: deny), so it presents profile info and tells Boss the exact command to run manually or via switch.bat.
---

## Purpose

Informational skill. Orchestrator CANNOT restart opencode itself (bash: deny). When Boss asks to switch profiles, the orchestrator tells Boss the exact command to run or points to `switch.bat` (Windows) / manual command (Linux/macOS).

The actual profile switch is a manual step outside opencode:
- **Windows**: double-click `switch.bat` or run it from terminal
- **Manual**: copy the desired profile to `opencode.jsonc`:
  ```bash
  cp profiles/opencode.{name}.jsonc opencode.jsonc && opencode
  ```
Then restart opencode.

## Process

1. Display the 4 profiles with their model assignments
2. Let Boss pick 1-4
3. Tell Boss the exact command to copy the profile or point to `switch.bat`
4. Remind Boss to restart opencode after switching

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
