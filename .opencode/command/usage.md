# /usage

Usage report request count per role dari opencode.db.

## Cara pakai
- Orchestrator panggil: `python .opencode/tools/usage_report.py` (di root farewell-orchestra)
- Argumen: `--today`, `--project <name>`, `--json`

## Konvensi report
Setiap report akhir ke Boss WAJIB menyertakan blok Usage Report (detail per role) di bagian bawah report, setelah Residual risk. Format: tabel Role | Requests | Cost | Tokens in/out (lihat output script).
