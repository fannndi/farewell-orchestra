# LESSONS.md — Error Log & Pattern Tracker

## Error Taxonomy

| Type | Contoh | Fix Pattern |
|------|--------|-------------|
| **HALLUCINATED_TOOL** | Agent invoke tool yg nggak ada | Recheck available tools, clarify brief |
| **MALFORMED_OUTPUT** | Format broken (no file:line, no tag) | Auto-retry format hint |
| **STALE_REFERENCE** | Referensi file/config basi | Sync audit, update references |
| **RUNAWAY_AGENT** | Loop 3x same intent | Loop guard triggered → STOP |
| **PERMISSION_BLOCK** | Tool call denied | Check agent permission matrix |
| **SILENT_REGRESSION** | Output beda dari expected | Verify acceptance criteria |

## Log

Format: `| Tanggal | Type | Trigger | Error | Root Cause | Fix |`

| Tanggal | Type | Trigger | Error | Root Cause | Fix |
|----------|------|---------|-------|------------|-----|
| 2026-07-27 | PERMISSION_BLOCK | Boss: "kok kamu gak bisa edit" | Executor blocked dari .config folder | external_directory config belum include Documents | Tambah `C:/Users/FANNNDI/Documents/**` ke global config |
| 2026-07-27 | STALE_REFERENCE | Audit opencode schema | compaction keys `keep.tokens` & `buffer` bukan schema valid | Config dibuat sebelum schema final | Migrasi ke `preserve_recent_tokens` & `reserved` |
| 2026-07-27 | STALE_REFERENCE | AGENTS.md table mismatch | Skill mapping di table AGENTS.md nggak akurat | Table nggak di-update saat skill ditambah | Fix researcher/reviewer/executor row |

*Append-only. Satu baris per insiden non-trivial. Jangan overwrite.*
