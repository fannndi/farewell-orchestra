# Project Guide — Farewell Orchestra sebagai Cross-Project Assistant

Repo ini adalah **otak orkestrasi Boss** — satu tempat, semua project. Buka opencode di sini, arahkan ke project target, orchestra yg kerja.

## Setup Sekali Jalan

Tambahin SEKALI di `~/.config/opencode/opencode.json`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "external_directory": {
      "~/projects/**": "allow",
      "~/Documents/**": "allow"
    }
  }
}
```

Ganti path sesuai folder tempat Boss biasa clone repo.

## Cara Pakai

### 1. Project baru (atau existing tanpa docs)

```
/new-project
```

Orchestrator bakal tanya nama, satu-liner, tech stack → generate 10 docs di `docs/` + `sub-project.md`.

### 2. Lanjutin project yg udah ada

```
/work-on <nama-project>
```

Contoh: `/work-on my-app`, `/work-on C:\Users\FANNNDI\projects\my-app`

Orchestrator resolve path, baca `sub-project.md`, tampilin context (fase, task aktif), siap nerima request.

### 3. Langsung kerja (tanpa context switch)

```
kerjain project ini C:\Users\FANNNDI\projects\my-app, tolong tambahin fitur X
```

Orchestrator deteksi path, baca anchor, langsung gas.

## Alur Kerja

1. Boss buka opencode di folder **farewell-orchestra**
2. Boss kasih `/work-on <project>` atau sebut path project
3. Orchestrator baca `sub-project.md` → dapet context (fase, task aktif, profile)
4. Kerja sesuai orchestration rules: anti-gigo → decompose → parallel researcher/reviewer → execute → report 3 baris
5. Executor update `sub-project.md` (Memori Agent, task aktif) tiap selesai

## File Penting

| File | Fungsi |
|------|--------|
| `templates/sub-project.md` | Template anchor — di-copy ke tiap sub-project, jadi otak-nya orchestra di project itu |
| `.opencode/command/work-on.md` | `/work-on` command — switch context ke sub-project |
| `.opencode/command/new-project.md` | `/new-project` command — scaffold 10 docs + sub-project.md |
| `.opencode/skills/bootstrap-project/` | Skill: generate 10 dokumentasi standar |

## Kapan TIDAK Perlu

Project kecil, sekali pakai, nggak butuh dokumentasi → skip `/new-project`. Langsung sebut path + request. Anti-GIGO tetep jalan.

## Tips

- Kalau lupa nama project, ketik `/work-on` kosong — orchestrator bakal tanya.
- `sub-project.md` adalah otak orchestra di project itu. Jangan dihapus.
- Path dengan spasi: gunakan quotes. Contoh: `/work-on "my app"`
- Profile (V1/Limited) dipilih pas `/new-project` atau bisa diganti manual di `sub-project.md`.
