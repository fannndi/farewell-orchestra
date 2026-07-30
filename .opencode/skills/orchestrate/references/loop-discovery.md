# Loop Discovery — Reference

> Referensi lengkap untuk §12 Loop Discovery Gate, §13 Runtime Loop Guard, dan §14 Legacy Loop Guard.
> Digunakan oleh orchestrator skill — dipisahkan agar SKILL.md tetap ringkas.

## §12. Loop Discovery Gate

Gunakan Loop Discovery ketika ada indikasi loop berulang atau schedulable engineering work.
Contoh pemicu:
- Prompt/u target sama muncul berulang
- Workspace entropy menunjukkan recurring friction point
- Sesi evidence menunjukkan pattern "stuck" berulang
- Review feedback menunjukkan berulang perlu perubahan tertentu

### 10-Point Decision Gate

1. **Repeated intent**: setidaknya dua kali serupa, atau task beresiko/tinggi kemungkinan muncul lagi
2. **Existing coverage**: bukti bahwa current Skills/hooks/commands/agents/docs TDK punya coverage
3. **Stable input**: loop bisa mulai dari evidence repeatable atau schedule/trigger
4. **Repeatable procedure**: steps repeatable, bukan investigation baru tiap kali
5. **Verification**: success punya check, report, patch, review, command, atau eksplisit "needs more evidence" boundary
6. **Stop condition**: loop bisa end on state, score, count, result, atau decision manusia
7. **Safety boundary**: permission, secret, external action, broad repo changes punya human gate kalau needed
8. **State contract**: paused atau multi-run work punya replayable input, checkpoint, artifact, atau history pointer; stateless loop katakan kenapa state unnecessary
9. **Observability contract**: logs, traces, spans, report, run directories, atau review artifacts show apa yang terjadi, which tools ran, what changed, dan kenapa loop stopped
10. **Evaluation contract**: automated check, LLM/human review, regression fixture, atau comparison criteria disebut sebelum iterative improvement direkomendasikan

Kalau evidence kurang, return `Needs more evidence`; jangan promote loop dari file age, line count, churn, cache paths, titles, counts sendiri.

### Runtime-Fit Check

Sebelum memilih owner, decide what kind of loop is actually needed:

- **Workflow loop**: steps mostly known. Prefer command, script, hook, rule, Skill-backed playbook, atau scheduled `/better-harness` follow-up over autonomous agent
- **Agent loop**: work needs flexible planning, tool use, handoffs, recovery from changing evidence. Require turn limits, tool boundaries, observable traces, clear final-output condition
- **Evaluator-optimizer loop**: iterative improvement useful only when there are explicit evaluation criteria and another pass measurably improves output
- **Scheduled or background loop**: cadence or event trigger exists, inputs non-interactive, side effects reversible or gated, loop can report completion or `needs more evidence`
- **Human-gated loop**: sensitive edits, shell commands, external writes, secrets, policy decisions, broad repo changes require approval before side effect happens
- **Skill-shaped loop**: durable asset procedural knowledge for agent to load; jangan treat Skill itself as runtime state, approval, tracing, scheduling

### Runtime-Fit Decision Tree

Keputusan berdasarkan evidence + runtime-fit:

- Jikalau evidence memenuhi 10 point AND evidence menunjukkan automation:
  - Siapkan schedule/hook/command untuk otomatisasi
  - Kalau siap, taruh di hooks.jsonc sebagai hook atau command
- Jikalau evidence memenuhi 10 point tapi runtime tidak cocok untuk automation:
  - Pilih owner berdasarkan runtime-fit check
- Jikalau evidence kurang, kembali needs more evidence

## §13. Runtime Loop Guard — 3x Trigger → Loop Discovery Gate

| Sinyal | Action |
|--------|--------|
| Agent+tool+intent sama 3x berturut-turut | STOP, invoke Loop Discovery Gate (§12) utk evaluasi apakah loop ini perlu durable owner |
| Executor gagal error identik 2x | Escalate ke researcher |
| Researcher balik hasil sama 2x | Udah cukup — jangan research lagi |
| Conversation muter tanpa progress | Report: "Stuck di [topik]. Perlu arahan." |
| Read file SAMA >3x tanpa nulis | Kurangi scope |
| Tool + argumen sama 2x tanpa progress | Kurangi scope atau ganti approach |

> **Runtime loop = STOP + design gate.** Setiap 3x trigger otomatis invoke Loop Discovery Gate (§12) untuk decide: skip, hook, script, atau skill?

## §14. Loop Guard (Legacy — kept for reference)

| Sinyal | Action |
|--------|--------|
| Agent+tool+intent sama 3x berturut-turut | STOP, tanya Boss |
| Executor gagal error identik 2x | Escalate ke researcher |
| Researcher balik hasil sama 2x | Udah cukup — jangan research lagi |
| Conversation muter tanpa progress | Report: "Stuck di [topik]. Perlu arahan." |

**Prinsip:** 3x sama = loop. Token lebih baik buat nanya Boss.
