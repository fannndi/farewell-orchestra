# # Design.md

## Ringkasan
**Software House Mini Architecture** — 4 agent coordination framework dengan skill specialization, permission matrix, dan scheduling simetris.

## Struktur Agent

| Agent | Mode | Model | Permission | Fokus |
|-------|------|-------|------------|-------|
| Orchestrator | primary | DeepSeek Flash | * deny (read:allow, skill:allow, question:allow) | Decompose, validate, Delegate |
| Researcher | subagent | 9router/oc/nemotron-3-ultra-free | * deny (read:allow, glob:allow, grep:allow) | Cross-file tracing, tech stack research |
| Reviewer | subagent | 9router/oc/nemotron-3-ultra-free | * deny (read:allow, websearch:allow) | STRIDE audit, convention enforcement |
| Executor | subagent | 9router/oc/nemotron-3-ultra-free | * deny (read:allow, edit:allow, bash:allow) | Implementasi YAGNI-first, ground-truth verification |

## Arus Proyek

```
Boss → Orchestrator (anti-gigo + decompose) → (Researcher + Reviewer) parallel → Orchestrator (synthesize) → Executor (implement)
```

## Skill Pipeline

| Skill | Agent | Trigger |
|-------|-------|---------| 
| anti-gigo | orchestrator | Boss request (before dispatch)
| grill | orchestrator | Input ambigu
| orchestrate | orchestrator | Anti-gigo pass
| minimal-impl | executor | Brief di-delegasikan
| verification-ground-truth | executor | Verification akses command output
| forensic | researcher | Deep debugging trigger
| web-research | researcher | Tech stack / web context needed
| stride-audit | reviewer | Security + architectural audit

## Konfigurasi

| Config | Path | Deskripsi |
|--------|------|------------| 
| Default config | opencode.jsonc | Paid profile (default) |
| Profile switching | switch.sh / switch.bat | Paid/Hybrid/Free copy |
| Agent persona | .opencode/agents/*.md | Deskripsi agent-specific |
| File anchor | sub-project.md | Konteks per-project |
| Global permission | ~/.config/opencode/opencode.json | External directory akses |

## Sambutan Kesalahan

| Error type | Trigger | Recovery |
|------------|--------|----------| 
| PERMISSION_BLOCK | Tool call deny | Periksa permission matrix |
| STALE_REFERENCE | File config basi | Sync audit, update references |
| LOOP_GUARD | 3x identik intent | STOP, report ke Boss |
| ESCALATION | Executor gagal 2x | Researcher deep debug |

## Standar Output

Format: `[LEVEL]/file:line — pesan` → Tingkat konsistensi

## Linting & Verifikasi

- Setiap executor report WAJIB verifikasi command output
- YAGNI ladder (minimalizam over-add)
- Delete-over-add: hapus 5 baris > tambah 3 baris
- Naming konsisten per file pattern
---