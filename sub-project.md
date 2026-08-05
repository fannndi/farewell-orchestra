# farewell-orchestra

State: mission control OpenCode - 4 agent, 11 skill, 5 profile (Pro/Codex Main/Daily/Eco/Backup). Refactor 2026-08-05: (1) cost-awareness & kategori free/paid dihapus dari layer agent - deny-by-default aktif di researcher/reviewer; (2) KISS: generate.py 954->751, persona dikompres (orchestrator 127->33), status.md merge ke check.md, hooks redundant dihapus (pre-generate, dispatch.ps1, session-end), skill 11 tetap apa adanya.

Executor: fix @verify tool — (1) verify.ts: cwd=context.worktree, timeout 15s->30s, detection python-first + spawnSync probe 2000ms (python3 = WindowsApps stub, terkonfirmasi exit 9009); (2) verify.py: normalize separator `\`->`/` + git subprocess timeout 15->5; test CLI pass, logika detection tested via node (python terdeteksi 13ms). Butuh restart OpenCode utk re-load plugin.

Executor: kompres orchestrate/SKILL.md 248->160 baris (hapus duplikat AGENTS.md, jadikan referensi 1 baris; pertahankan ping guard/verify gate/fallback/brief 5-field/blast radius/peer debate/loop guard/proactive), AGENTS.md +1 baris pengerem global ("Usul, jangan eksekusi").
