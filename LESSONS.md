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
| 2026-07-28 | STALE_REFERENCE | Boss: "bisa nggak context limit free dinaikan 1m" | oc/nemotron-3-ultra-free model ID not found on 9Router — 5/7 agents failed silent on free profile. Also affected hybrid/main compaction agent. | Model `oc/nemotron-3-ultra-free` doesn't exist on 9Router gateway. OpenRouter free model `nvidia/nemotron-3-ultra-550b-a55b:free` has 1M context but was configured as 128K. | Replace all `oc/nemotron-3-ultra-free` refs with `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`. Bump context_limit to 1M. Remove non-existent model from provider list. |
| 2026-07-28 | SILENT_REGRESSION | Context size mismatch analysis | OpenRouter docs & API report 1M context for nemotron-3-ultra-free, but 9Router gateway caps at 128K reported. Config followed 9Router cap, causing 87.5% context loss. | 9Router proxy cap vs actual model capability mismatch. | Config now set to 1M to match OpenRouter actual. If 9Router enforces 128K at API level, OpenCode will still manage context better knowing the true model limit. |
| 2026-07-28 | MALFORMED_OUTPUT | Free profile performance analysis | tool_output max_bytes:38400 terlalu kecil — sering truncate tool results causing agents kerja dengan incomplete data. Compaction preserve_recent_tokens:5000 terlalu agresif — context loss antara turns. | Conservative default settings nggak tuned untuk agentic workflow. | Bump tool_output ke 51200 bytes, compaction preserve ke 7000, reserved ke 20000. |

| 2026-07-28 | Profile rework: drop paid+free, 4 hybrid variants | Config drift — paid terlalu expensive untuk student budget | Budget constraint mismatch | Created 4 hybrid variants (hybrid-v1 to v4) dengan deepseek-v4-flash sebagai primary orchestrator hanya, semua sub-agen pake free models. Update opencode.jsonc, switch.bat, switch.sh. |
| 2026-07-28 | Final elimination: V1 winner setelah stress test | N/A | N/A | Setelah stress test berat di semua 4 role agent, V1 (deepseek-v4-flash + deepseek-free + north-mini-code) dipilih sebagai pemenang. Profiles/, switch.bat, switch.sh dihapus. Hanya opencode.jsonc kept. |
| 2026-07-28 | minimax-m3 small context | orchestrator context 128K instead of 1M | limit.context hardcoded conservative default | set limit.context=1000000 to match Flash premium tier |

*Append-only. Satu baris per insiden non-trivial. Jangan overwrite.*