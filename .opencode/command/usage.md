# /usage

Usage report request count per role dari opencode.db.

## Cara pakai
- Orchestrator panggil: `python .opencode/tools/usage_report.py` (di root farewell-orchestra)
- Argumen: `--today`, `--project <name>`, `--json`
- Mekanisme `'+'` (delta sesi): `--delta` atau `--since <ts>`
  - `--delta`: delta request sejak marker `.opencode/.usage-marker`, lalu update marker (run pertama: marker = now, delta = 0)
  - `--since <ts>`: delta request sejak timestamp eksplisit (epoch ms atau `'YYYY-MM-DD HH:MM:SS'` UTC)

## Konvensi report
Setiap report akhir ke Boss WAJIB menyertakan blok Usage Report (detail per role) di bagian bawah report, setelah Residual risk. Format: tabel Role | Requests | Cost | Tokens in/out (lihat output script).

Dengan `--delta`/`--since`, tabel memakai format total + delta sesi: `Role | Total | +Delta (sesi) | = Total baru | Cost | Tokens in/out`, contoh: `orchestrator | 2,895 | +5 | 2,900 | $0.00 | 12k / 3k`.

## Footer report (wajib)
Orchestrator WAJIB jalankan `python .opencode/tools/usage_report.py --delta` di akhir setiap report dan tempel output sebagai footer. Ini bagian dari disiplin report — bukan opsional.
