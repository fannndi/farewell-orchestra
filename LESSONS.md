# Lessons Learned

> Auto-log oleh orchestrator via executor setiap insiden non-trivial (architectural fix, systemic bug, pattern detection).
> Skip typo/trivial. Satu baris per entry.

| date | trigger | error | root cause | fix |
|------|---------|-------|------------|-----|
| — | — | — | — | — |
| 2026-07-29 | Stress test model — 6 OC + 4 OR free | nemotron-550b:free FAIL (reasoning overflow, output kosong). north-mini-code-free: JUARA (JSON clean, tool call). | Model reasoning-heavy overflow di max_tokens rendah. OR nemotron butuh >500 tok. | Ganti semua nemotron-550b:free → gpt-oss-20b:free. Tetap pake north-mini-code-free/OR untuk reviewer. |
| 2026-07-29 | Cross-project optimasi — audit 10 gaps + 3 BLOCKING | project-guide.md missing, templates/ missing, LESSONS.md missing, hardcode path, profile mismatch, permission boundary lemah, path traversal tanpa proteksi | Dokumentasi janji vs realita: file referenced tapi tidak ada. Path resolution tanpa sanitasi. Permission boundary global-only. | Bikin 3 file baru (project-guide, templates/sub-project, LESSONS). Fix orchestrator.md step 0 dengan path traversal protection + audit log. Update opencode.jsonc, bootstrap-project skill, AGENTS.md, README.md. Hapus helper-mode/ stale. |
| 2026-07-29 | Libur — optimasi orchestra 5 item | Timeout/tool fail ga tertangani, AGENTS.md gemuk, Memori Agent tipis, context purge ga ada | Error handling masih umum, dokumen redundan, memory cuma 1 line | Tambah auto-recovery timeout+tool fail di executor + minimal-impl + orchestrator. Compress AGENTS.md + agent files. Tambah Keputusan & Konteks di sub-project.md. Context purge protocol di path check. |
| 2026-07-29 | Optimasi lanjutan — tool redundancy + skill kompres + step budget + check command | Skill files verbose (252 total lines), step budget kebesaran buat sesi 30 menit, check.md referensi profile lama | Tool redundancy belum ada aturan, skill lazy-loaded tapi masih gemuk | Tambah Dispatch Rules di orchestrator. Kompres 4 skill (252→219 lines). Step budget: 20/18/14/18 di 7 file. check.md update 6 profile + budget. |
| 2026-07-29 | Adaptasi better-harness (QoderAI) — blast radius + work loop + evidence levels | Farewell-orchestra gak punya impact analysis, quality gates, atau evidence scoring | Better-harness punya 3 fitur yg farewell-orchestra belum punya | Adaptasi blast radius pre-check di orchestrate skill. Agent Work Loop (5 gates) sebagai quality gate. Evidence levels (Present/Wired/Exercised/Outcome) di forensic skill. |
| 2026-07-29 | Adaptasi better-harness putaran 2 — blast radius upgrade, work loop 15 check, evidence bundle | Adaptasi pertama cuma superficial (grep blast radius, 5 gate, 4 level) | Better-harness pake tree-sitter AST + BFS call graph + scoring engine — gue cuma baca file doang pas pertama | Upgrade blast radius: import-based graph + BFS traversal + scoring + core rules + test gap. Work loop: 5→15 checks. Evidence bundle: 4 lane pre-execution context. |
| 2026-07-29 | Enhance audit skill — Depth Assurance Protocol + skeptic layer + evidence depth tags | Audit better-harness cuma baca README — dangkal, gak baca kode asli. Boss tegur. | Reviewer gak punya protokol buat mencegah audit superficial | Tambah Depth Assurance (3 pass: Scan→Detail→Cross-Reference). Skepticism Layer: docs bohong sampai terbukti. Evidence depth tags [D1-D4]. Self-check sebelum report. |
| 2026-07-30 | Audit + eksekusi 6 optimasi (P1+P2) | learn.ts pakai shell type/set-content, prune_rules missing, hardcode threshold di check/hook, BFS no early-stop, step budget flat | Sub-tool implementation fragile (shell wrapper), generator boilerplate stale, doc-as-config drift | Refactor learn.ts ke pure Node FS + strict regex YYYY-MM-DD. Tambah prune_rules (tool_output head/tail, file_lists collapse). Baca step budget dari opencode.jsonc. Early-stop BFS >25 affected atau depth>2. Scale step budget by task size (TRIVIAL=8, LARGE=25). |
| 2026-07-30 | Boss komplain session break terus-menerus — "malah merepotkanku" | Session Break Protocol auto-trigger setiap kena step limit (O:22, R:24, V:20, E:25). Boss report "selalu disuruh ke next session" — ini friction. | Step budget terlalu kecil untuk sesi real. Session Break Protocol wajib jalan otomatis di step limit tanpa tanya Boss dulu. | Naikkan step budget drastis: O:22→500, R:24→400, V:20→400, E:25→500. Ubah Session Break Protocol dari mandatory → optional (trigger only kalau Boss bilang stop). Scale step budgets by task size ditambah level MASSIVE. — verify:pass `read opencode.jsonc + orchestrator.md + AGENTS.md — budget tercermin di 3 file, session break jadi manual trigger` |
| 2026-07-30 | Boss komplain orchestrator kerja sendiri tanpa dispatch free model — log model 100% ocg/deepseek-v4-flash, 0% north-mini-code-free/nemotron-3-ultra-free | Orchestrator (paid) nulis kode, baca file, debug stress test — semua tugas yg free sub-agent bisa kerjain. Cost bocor, arsitektur dilanggar. | AGENTS.md gak eksplisit soal cost. Pengecualian "1 baris typo fix" terlalu longgar. Gak ada mekanisme deteksi orchestrator kerja sub-agent. | 1) Cost Model section di AGENTS.md — paid vs free eksplisit. 2) Freeze Rule — orchestrator never writes code, tabel boleh/tidak boleh. 3) Cost guard di Safety & Guardrails. 4) orchestrator.md — Cost Awareness section, forbidden rules diperkuat. 5) SKILL.md — cost rule di header. — verify:pass `stress test 5/5 PASS + grep 'orchestrator.*edit\|write\|bash' di doc — harus nol` |





## Sensor Coverage Checklist

> Audit: mekanisme kontrol apa yg kita punya vs standar harness engineering 2026.
> Legend: ✅ ada | ⚠️ parsial | ❌ belum

| Sensor Type | Kita Punya? | Keterangan |
|-------------|------------|------------|
| **Guides (feedforward)** | | |
| AGENTS.md project rules | ✅ | 37 line, slim |
| Agent persona files | ✅ | 4 agent, masing-masing |
| Skills (on-demand) | ✅ | 9 skill files, lazy-loaded |
| Step budgets | ✅ | O:500, R:400, V:400, E:500 |
| Tool permissions | ✅ | Terbaru: scoped (researcher/reviewer no edit) |
| **Sensors (feedback)** | | |
| JSON validation (generate.py) | ✅ | Temp→validasi→copy |
| Post-generate hook | ✅ | Baru: `.opencode/hooks/post-generate.ps1` |
| Custom tool: harness_status | ✅ | Baru: `.opencode/tools/harness_status.ts` — validate, profile, sensor cek |
| Custom tool: learn | ✅ | Baru: `.opencode/tools/learn.ts` — log lesson struktur ke LESSONS.md |
| verification-ground-truth skill | ⚠️ | Ada tapi cuma di executor |
| STRIDE audit (reviewer) | ⚠️ | Manual, bukan otomatis |
| doom_loop (built-in) | ✅ | Baru: `"deny"` — auto-block loop 3x tanpa nanya |
| **Missing Sensors** | | |
| PreToolUse/PostToolUse hooks | ❌ | OpenCode gak support hooks system |
| Loop detection heuristic | ⚠️ | doom_loop built-in udah, heuristic manual di orchestrator.md |
| Exponential backoff | ⚠️ | Baru di docs, belum otomatis |
| Automated rollback | ❌ | Kalau generate gagal, gak ada undo |
| Cost tracking | ❌ | Gak tau berapa token tiap session |
| CI/CD integration | ❌ | Gak ada test di pipeline |
| **Orchestration** | | |
| Fan-out parallel | ✅ | Researcher+reviewer parallel |
| Escalation path | ✅ | Executor→Researcher→Boss |
| No-op detection | ✅ | Skip kalo profile sama |
| Context isolation | ✅ | sub-project.md anchor |
| Session memory | ⚠️ | Cuma LESSONS.md + sub-project.md |
| **Recovery** | | |
| Temp→copy atomic write | ✅ | generated file aman |
| Retry logic | ✅ | 1x auto-retry di executor |
| Exponential backoff | ⚠️ | Baru di docs, belum otomatis |
| Checkpoint-resume | ❌ | Gak ada state persistence antar sesi |
