# Farewell Orchestra

An OpenCode agent orchestration framework. Manage 4 specialized agents (orchestrator, researcher, reviewer, executor) with explicit, GIGO-enforced workflows for safe, deterministic delegation.

## How to Use

Just run `opencode` in this directory. Boss gives tasks, orchestrator validates then decomposes, reviewer+researcher audit in parallel, executor implements YAGNI-first. One command, autonomous coordination.

## Model Configuration

- **Orchestrator**: deepseek-v4-flash
- **Sub-agents** (researcher, reviewer, executor): use free models

## Switching Profiles

Run `switch.bat` (Windows) or `switch.sh` (Linux/macOS) to switch between Free, Hybrid, and Paid profiles.

## Quick Reference

| Variant | Description | Model Config |
|---------|-------------|--------------|
| Free | Solo(executor) | Free model |
| Free + 1 | Executor + Researcher | Free + Free |
| Free + 2 | Executor + Reviewer | Free + Free |
| Free + 3 | Full orchestration | Free + Free + Free |
| Hybrid + 1 | Solo(executor) + Free researcher | Free + Free |
| Hybrid + 2 | Solo(executor) + Free reviewer | Free + Free |
| Hybrid + 3 | Solo(executor) + Free orchestration | Free + Free + Free |
| Paid | Full orchestration + Paid orchestrator | Paid + Free |

## Examples

```bash
# Simple task
opencode "Fix this"

# Explain a pattern
opencode "Explain [file:line]"

# Test setup
opencode "/check"</command>