# Farewell Orchestra

Multi-agent orchestration: 4 agent, 6 skill, 1 pipeline.

## Philosophy

1. **Goal-Oriented** — fokus ke tujuan akhir
2. **Proaktif** — ambil inisiatif
3. **KISS** — simple itu lebih baik

## Pipeline

```
Request → prepare → [research || review] → orchestrate → implement → report
```

## Roles

| Agent | Tugas | Tulis Kode? |
|-------|-------|:-----------:|
| Orchestrator | Atur tim | ❌ |
| Researcher | Cari bukti | ❌ |
| Reviewer | Cari masalah | ❌ |
| Executor | Tulis kode | ✅ |

## Rules

1. **Freeze Rule** — Orchestrator tidak nulis kode
2. **Evidence** — Klaim WAJIB punya file:line
3. **Trust** — Sub-agent mampu, jangan ambil alih
4. **Verify** — Tidak ada "done" tanpa bukti

## Cross-Project

Cukup bilang "aku mau kerja di project X" — sistem otomatis:
1. Cek docs
2. Kalau tidak ada → reverse engineer → generate docs
3. Lanjut kerja
