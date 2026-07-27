# LESSONS.md — Error Log & Pattern Tracker

Format: `| Tanggal | Trigger | Error | Root Cause | Fix |`

| Tanggal | Trigger | Error | Root Cause | Fix |
|----------|---------|-------|------------|-----|
| 2026-07-27 | Boss: "kok kamu gak bisa edit" | Executor blocked dari .config folder | external_directory config belum include Documents | Tambah `C:/Users/FANNNDI/Documents/**` ke global config |
| 2026-07-27 | Audit opencode schema | compaction keys `keep.tokens` & `buffer` bukan schema valid | Config dibuat sebelum schema final | Migrasi ke `preserve_recent_tokens` & `reserved` |
| 2026-07-27 | AGENTS.md table mismatch | Skill mapping di table AGENTS.md nggak akurat | Table nggak di-update saat skill ditambah | Fix researcher/reviewer/executor row |

*Append-only. Satu baris per insiden non-trivial. Jangan overwrite.*
