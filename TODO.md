# TODO — Next Session

## 1. Loop Discovery Gate
**Upgrade loop guard** dengan Better Harness 10-point decision gate + runtime-fit check.

- [ ] Tambah `Loop Discovery Gate` section ke `.opencode/skills/orchestrate/SKILL.md`
- [ ] 10-point gate: repeated intent, coverage, input stability, procedure, verification, stop, safety, state, observability, evaluation
- [ ] Runtime-fit check: workflow vs agent vs evaluator-optimizer vs scheduled vs human-gated
- [ ] Update loop guard di `.opencode/agents/orchestrator.md` — ganti "3x sama = STOP" dengan decision gate
- [ ] Verify: `python .opencode/scripts/check-links.py` still passes

References:
- `source/better-harness/references/loop-engineering/loop-discovery.md`
- `source/better-harness/references/loop-engineering/README.md`

---

## 2. Hook Lifecycle Events
**Event-driven hook system** — terinspirasi dari Zero's beforeTool/afterTool/sessionStart/sessionEnd.

- [ ] Buat `.opencode/hooks/hooks.jsonc` — definisi hook events
  ```jsonc
  { "hooks": [
    { "id": "pre-generate", "event": "beforeGenerate", "command": "powershell -File .opencode/hooks/pre-generate.ps1" },
    { "id": "post-generate", "event": "afterGenerate", "command": "powershell -File .opencode/hooks/post-generate.ps1" },
    { "id": "check-links", "event": "beforeCommit", "command": "python .opencode/scripts/check-links.py" }
  ]}
  ```
- [ ] Buat `.opencode/hooks/dispatch.ps1` — dispatcher yang baca hooks.jsonc, filter by event, execute hooks, check exit codes
- [ ] Buat `.opencode/hooks/pre-generate.ps1` — validasi sebelum generate (profiles.json syntax check)
- [ ] Integrasi `dispatch.ps1` ke `profiles/generate.py` — panggil dispatch sebelum/sesudah generate
- [ ] Export architecture pattern dari Zero: payload via stdin JSON, exit 0=continue, non-zero=block
- [ ] Verify: `python profiles/generate.py default-oc` triggers pre + post hooks

References:
- `source/zero/internal/hooks/dispatch.go` — event types, payload format, blocking logic
- `source/zero/docs/EXTENDING.md` — hook config format
- `source/zero/internal/hooks/hooks.go` — event constants, audit status

---

## 3. Integrate Doc Link Checker
**Wire check-links.py ke dalam project workflow.**

- [ ] Tambah `python .opencode/scripts/check-links.py` ke `.opencode/command/check.md` section 7 (atau section baru)
- [ ] Opsional: integrasi ke `hooks.jsonc` sebagai `beforeCommit` event (tergantung #2 selesai)
- [ ] Tambah ke `profiles/generate.py` sebagai post-generate validation step
- [ ] Verify: `python .opencode/scripts/check-links.py` exit 0

---

## Acceptance Checklist (end of session)

- [ ] `python .opencode/scripts/check-links.py` — OK, 0 broken
- [ ] `python profiles/generate.py --validate` — OK, 6 profiles
- [ ] Semua perubahan commit + push
- [ ] Update file ini: checklist items checked
