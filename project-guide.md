# Project Guide — Farewell Orchestra sebagai Cross-Project Assistant

Repo ini bukan cuma config buat dirinya sendiri — ini **otak orkestrasi Boss** yang dipanggil dari project lain mana pun, tanpa di-copy ulang ke tiap repo.

## Setup Sekali Jalan

### Opsi C — Tetap di workspace farewell-orchestra, kasih path per pesan (yang dipakai Boss)
Jalanin `opencode` di dalam folder farewell-orchestra seperti biasa, terus input: `"bantu aku kerjain project ini <path>"`. Orchestrator treat path itu sebagai target root (lihat AGENTS.md Session Flow step 0).

Wajib disetup dulu — OpenCode scoped ke cwd tempat dia di-start; akses ke path lain trigger `permission.external_directory` (default "ask" = prompt tiap kali). Biar nggak prompt terus, tambah SEKALI di `~/.config/opencode/opencode.json` (global, bukan di tiap profile):
```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "permission": { "external_directory": { "~/projects/**": "allow" } }
}
```
Ganti `~/projects/**` ke folder tempat Boss biasa clone repo. Berlaku ke semua profile karena ini setting workspace-level, bukan per-agent.

Alternatif yang lebih formal (belum diverifikasi hands-on): fitur native **references** (`path`/`repository` alias di opencode.json) — cek `opencode.ai/docs/references` sebelum diandalkan.


### Opsi A — Alias per-profile (recommended, zero-copy)
Config profile (`profiles/*.jsonc`) berlaku di project mana pun karena `-c` cuma nunjuk file config, bukan project. Cwd tetap project target — orchestra cuma nyuplai "otak"-nya.

Tambah ke `~/.bashrc`:
```bash
FO=~/farewell-orchestra   # sesuaikan path clone lo
alias ocp="opencode -c $FO/profiles/opencode.paid.jsonc"
alias och="opencode -c $FO/profiles/opencode.hybrid.jsonc"
alias ocf="opencode -c $FO/profiles/opencode.free.jsonc"
```
Jalankan dari root project lain: `cd ~/project-lain && och`

> Belum diverifikasi: apakah `-c` merge atau full-replace kalau project target juga punya `opencode.json` sendiri. Cek `opencode --help` atau test langsung sebelum diandalkan di project yang udah ada config-nya.

### Opsi B — Global reach (persona+skill otomatis di semua project)
Symlink (jangan copy — biar nggak ada duplikasi yang bisa out-of-sync):
```bash
ln -s ~/farewell-orchestra/.opencode/agents ~/.config/opencode/agents
ln -s ~/farewell-orchestra/.opencode/skills ~/.config/opencode/skills
```
Efeknya: 4 persona + skill farewell-orchestra ke-load di project APAPUN tanpa flag `-c`. Profile (model tier) tetap perlu dipilih manual — global config cuma bawa persona/skill, bukan model selection. Kombinasikan sama Opsi A buat profile switching.

Catatan: AGENTS.md project target (kalau ada) tetap kebaca terpisah — OpenCode jalan ke atas dari cwd nyari AGENTS.md sendiri. Jadi orchestrator dapet 2 layer: persona farewell-orchestra (global) + rules project lokal.

## Prompt Integrasi

Taruh ini di `AGENTS.md` project target, atau paste sebagai pesan pertama sesi baru:

```
Kamu adalah Farewell Orchestra — sistem 4-agent (orchestrator/researcher/reviewer/executor)
milik Boss, dikonfigurasi di ~/farewell-orchestra.

Project ini adalah salah satu sub-project Boss. Baca `sub-project.md` di root buat context
(fase, profile aktif, docs yang ada). Kalau belum ada, tawarin `/new-project` buat scaffold
10 dokumentasi standar (PRD/Architecture/Design/Schema/Rules/API_Contract/Tasks/Tests/
Context/debug) sebelum mulai coding.

Ikuti orchestration rules farewell-orchestra: anti-gigo dulu, decompose, parallel
researcher+reviewer, delegasi ke executor, report 3 baris.
```

## Onboarding Sub-Project Baru

1. `cd` ke root project (baru atau existing), jalanin orchestra (Opsi A/B).
2. `/new-project` — orchestrator jalanin `anti-gigo` (validasi nama/scope/tech stack), lalu skill `bootstrap-project`.
3. Executor nulis 10 file ke `docs/` + generate `sub-project.md` dari `templates/sub-project.md`.
4. Sesi berikutnya: orchestrator baca `sub-project.md` duluan sebelum kerja apapun — itu anchor context, bukan `AGENTS.md` (yang isinya rules farewell-orchestra sendiri, bukan state project).

## Kapan TIDAK Perlu Ini

Project kecil, sekali pakai, atau nggak butuh dokumentasi formal → skip `/new-project`, langsung kerja biasa. Anti-GIGO tetep jalan, tapi 10-file docs itu overhead yang cuma worth it buat project yang bakal dilanjutin lintas-sesi.

## File Map (tambahan)

| File | Fungsi |
|------|--------|
| `project-guide.md` | Panduan ini — cara pakai orchestra lintas-project |
| `templates/sub-project.md` | Template anchor file, di-copy ke tiap sub-project |
| `.opencode/skills/bootstrap-project/SKILL.md` | Skill: generate 10 docs dari project idea |
| `.opencode/command/new-project.md` | Slash command pemicu bootstrap |
