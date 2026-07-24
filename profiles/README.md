# Profiles

Switch model hanya dengan **copy file teks** — tidak perlu edit opencode.jsonc.

```
# Pro (default): orchestrator=Pro,  workers=Flash
copy profiles\pro-heavy.txt profiles\current-heavy.txt
copy profiles\pro-light.txt profiles\current-light.txt

# Flash: orchestrator=Flash, workers=Free
copy profiles\flash-heavy.txt profiles\current-heavy.txt
copy profiles\flash-light.txt profiles\current-light.txt

# Free: all Free (max hemat)
copy profiles\free-heavy.txt profiles\current-heavy.txt
copy profiles\free-light.txt profiles\current-light.txt

# Custom: edit langsung current-heavy.txt + current-light.txt
```

## File Matrix

| File               | Pro      | Flash    | Free     |
|--------------------|----------|----------|----------|
| `current-heavy.txt` | `ocg/deepseek-v4-pro` | `ocg/deepseek-v4-flash` | `oc/deepseek-v4-flash-free` |
| `current-light.txt` | `ocg/deepseek-v4-flash` | `oc/deepseek-v4-flash-free` | `oc/deepseek-v4-flash-free` |

## Role Mapping

| Tier  | Roles                                              | Source         |
|-------|----------------------------------------------------|----------------|
| Heavy | orchestrator                                       | current-heavy.txt |
| Light | researcher, reviewer, executor, title, summary, compaction | current-light.txt |
| Free  | build, plan, general, explore                      | (model bebas)  |

## Tambah Model Baru

1. Daftarkan di `provider.models` di `../opencode.jsonc`
2. Edit `current-heavy.txt` atau `current-light.txt` langsung
3. Atau buat preset baru: copy `pro-heavy.txt` → `custom-heavy.txt`, edit, lalu copy ke `current-heavy.txt`
