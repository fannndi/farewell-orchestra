---
name: cost
description: Cost tracking summary from temp dir log
---

# /cost — Cost Tracking Summary

Menampilkan ringkasan biaya dari cost-log.json di temp dir.

## Usage
/cost — tampilkan ringkasan semua sesi
/cost last — tampilkan sesi terakhir saja

## Output Format
Session  | Orchestrator     | Researcher     | Reviewer       | Executor       | Est. Cost
2026-08-01 | 234/500 (ocg/v4) | 89/400 (north) | 0/400 (nemotron) | 156/500 (nemotron) | $0.35

## Notes
- Cost log disimpan di %TEMP%\opencode\cost-log.json (Windows) atau $TEMP/opencode/cost-log.json (Unix)
- Estimasi biaya berdasarkan model pricing (approximate)
- Hanya mencatat kalau orchestrator eksplisit log
