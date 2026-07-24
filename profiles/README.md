# Profiles

Switch profile dengan copy ke `.env` di root:

```
copy profiles\pro.env ..\.env       # Pro:  orchestrator=Pro,  workers=Flash
copy profiles\flash.env ..\.env     # Flash: orchestrator=Flash, workers=Free
copy profiles\free.env ..\.env      # Free:  all Free (max hemat)
copy profiles\custom.env ..\.env    # Custom: edit dulu, bebas mix-match
```

## Profile Matrix

| Profile  | orchestrator (HEAVY)       | 7 workers (LIGHT)            |
|----------|---------------------------|-----------------------------|
| **pro**  | `ocg/deepseek-v4-pro`    | `ocg/deepseek-v4-flash`     |
| **flash**| `ocg/deepseek-v4-flash`  | `oc/deepseek-v4-flash-free` |
| **free** | `oc/deepseek-v4-flash-free` | `oc/deepseek-v4-flash-free` |
| **custom** | bebas                   | bebas                        |

## Tambah Model Baru

1. Daftarkan di `provider.models` di `../opencode.jsonc`
2. Tambah profile baru di sini (copy custom.env → rename)
3. Atau edit `custom.env` untuk mix-match
