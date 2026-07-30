# Next Session — 2026-07-30

## Pending improvements (optimal buat project baru)

- [ ] **Test: backup rollback** — `python profiles/generate.py default-oc` → cek `profiles/backups/` ada backup baru
- [ ] **Test: `python -m pytest tests/ -q`** — 18 tests harus tetap hijau
- [ ] **Doc/skill compression** — compress `.opencode/skills/orchestrate/SKILL.md` (190 baris), ekstrak detail ke file referensi
- [ ] **Integrasi CI** — `.github/workflows/test.yml`: `pytest tests/` + `check-links.py` tiap push
- [ ] **Rollback CLI** — tambah `python profiles/generate.py --rollback` untuk restore dari backup terakhir

## Dari evaluasi arsitektur

| Item | Status | Prioritas |
|------|--------|-----------|
| Backup rollback | ✅ Done | — |
| Test coverage (18 tests) | ✅ Done | — |
| Naming consistency | ✅ Done | — |
| Doc/skill compression | ❌ Pending | Medium |
| CI integration | ❌ Pending | Low |
| Rollback CLI (`--rollback`) | ❌ Pending | Low |
