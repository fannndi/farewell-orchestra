# Project Guide — Farewell Orchestra

Repo ini adalah **otak orkestrasi** — satu tempat, semua project. Buka opencode di sini, arahkan ke project target via `/work-on` atau `/new-project`.

## Setup Sekali Jalan

Tambahin SEKALI di `~/.config/opencode/opencode.json`:

```jsonc
{
  "permission": {
    "external_directory": {
      "~/projects/**": "allow",
      "~/Documents/Farewell-Knowlage/**": "allow"
    }
  }
}
```

## Cara Pakai

### 1. Project baru

```
/new-project
```

Orchestrator tanya nama, satu-liner, tech stack → generate 10 docs + sub-project.md.

### 2. Lanjutin project existing

```
/work-on <nama-project>
```

### 3. Langsung kerja

```
kerjain project ini ~/projects/my-app, tambahin fitur X
```

## Pipeline

```
Request → prepare → [research || review] → orchestrate → implement → report
```

## Skills

| Skill | Fungsi |
|-------|--------|
| prepare | Input validation + chunking |
| research | Codebase + web research |
| review | STRIDE audit |
| implement | YAGNI + verify |
| orchestrate | Decompose + dispatch |
| bootstrap-project | Scaffold docs |
