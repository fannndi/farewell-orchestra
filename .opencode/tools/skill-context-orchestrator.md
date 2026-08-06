# Skills: orchestrator

=== prepare ===
---
name: prepare
description: Use when receiving a request — validate input, extract requirements, chunk if needed. Gate before orchestration.
---
Gate awal sebelum dispatch. Flow:
```
Request → Cross-Project? → YES → Check Docs → Reverse Engineer? → Generate → Normal Flow
                ↓ NO
         Input Validation → HOLD? STOP. PARTIAL? → Grill. PASS? → Chunk → Dispatch
```
Kalau LLM tidak bisa handle complex instructions:
1. **Cek** — request punya goal dan scope?

=== orchestrate ===
---
name: orchestrate
description: Use after prepare passes — decompose, fan-out parallel, synthesize, brief executor.
---
Input sudah CLEAN. Flow:
```
Decompose → Evidence Bundle → Ping → Fan-Out → Synthesize → Verify Gate → Brief Executor → Post-Flight
```
Kalau LLM tidak bisa handle complex instructions:
1. **Decompose** — pecah task jadi 2-3 bagian kecil
2. **Fan-Out** — dispatch researcher + reviewer (atau salah satu)
3. **Synthesize** — gabung hasil, max 3 bullet

=== kiss-checklist ===
---
name: kiss-checklist
description: Pre-implementation checklist. WAJIB sebelum nulis kode.
---
WAJIB sebelum nulis kode. Cek semua.
- [ ] **Goal jelas?** — Apa yang mau dicapai?
- [ ] **Scope kecil?** — Bisa 1 file? Bisa 10 baris?
- [ ] **Existing solution?** — Udah ada yang bisa dipakai?
- [ ] **Dependency perlu?** — Bisa tanpa dependency baru?
- [ ] **Pattern perlu?** — Bisa tanpa pattern?
| Kondisi | Keputusan |

=== complexity-budget ===
---
name: complexity-budget
description: Limit complexity per feature. Kalau melebihi, pecah atau sederhanakan.
---
Limit complexity per feature. Kalau melebihi, pecah atau sederhanakan.
| Metric | Budget | Action kalau melebihi |
|--------|--------|----------------------|
| Files | ≤ 3 | Gabung atau pecah jadi sub-feature |
| Lines | ≤ 300 | Sederhanakan atau pecah |
| Functions | ≤ 10 | Gabung atau pecah |
| Dependencies | ≤ 5 | Hapus yang tidak perlu |
| Abstraction layers | ≤ 2 | Hapus abstraction |

=== progress-tracker ===
---
name: progress-tracker
description: Persistent task tracking. Track progress across sessions.
---
Persistent task tracking. Track progress across sessions.
```markdown
- [x] Step 1: [deskripsi]
- [x] Step 2: [deskripsi]
- [ ] Step 3: [deskripsi] — BLOCKED: [alasan]

=== error-handler ===
---
name: error-handler
description: Error classification + recovery. Handle errors differently based on type.
---
Error classification + recovery. Handle errors differently based on type.
| Type | Description | Recovery |
|------|-------------|----------|
| **RETRY** | Transient error, might work on retry | Retry dengan prompt lebih detail |
| **FALLBACK** | Error yang bisa di-handle dengan cara lain | Gunakan alternative approach |
| **ESCALATE** | Error yang butuh Boss intervention | Escalate ke Boss |
| **SKIP** | Error yang bisa di-skip | Skip, lanjut ke step berikut |
| **ABORT** | Error yang fatal, tidak bisa dilanjut | Stop, report ke Boss |

=== context-manager ===
---
name: context-manager
description: Context prioritization. Manage context across sessions.
---
Context prioritization. Manage context across sessions.
| Priority | Context | Keep | Drop |
|----------|---------|------|------|
| 1 (Critical) | Current task, blockers | Always | Never |
| 2 (High) | Recent decisions, active context | Usually | Only if full |
| 3 (Medium) | Historical context | Sometimes | If not relevant |
| 4 (Low) | Old sessions, completed tasks | Rarely | Usually |