# Smoke Test — Agent Personalities

Simulasi interaksi antar agent dengan personality baru.

---

## Skenario 1: Request ambigu → Orchestrator tolak

**Boss:** "perbaikin"

**🧙‍♂️ Orchestrator (Anti-GIGO):**
> HOLD. "Perbaikin" itu bukan instruksi. Itu cuma kata kerja tanpa objek.
> Goal: perbaikin *apa*?
> Scope: file/folder *mana*?
> Acceptance: gimana gue tahu udah bener?
> 
> Coba lagi. Satu kalimat. Goal, scope, acceptance.

---

## Skenario 2: Executor bikin fitur sederhana

**Orchestrator→Executor brief:**
```
Task: tambah tombol "Save" di halaman settings
Files: src/app/settings/page.tsx
Constraints: pakai komponen Button yg udah ada, jangan bikin component baru
Verify: npm run build -- pastiin nggak error
```

**👷‍♂️ Executor:**
> Ngerti. Tambah Button di settings page. Pakai yg udah ada. Nggak bikin component baru.
> 
> Done. 1 file changed.
> Verify: build passes.

---

## Skenario 3: Researcher cek library

**Orchestrator→Researcher brief:**
```
Cek apakah library "jsonwebtoken" masih ok buat auth, atau ada alternatif lebih baik.
```

**🕵️‍♂️ Researcher:**
> `package.json:15` — jsonwebtoken v9.0.2, last publish 2024-08.
> GitHub: 18k stars, masih maintained. Tapi ada issue #1023 soal timing attack di verify().
> npm advisory: nggak ada CVE aktif.
> Alternatif: jose (native Web Crypto, 2x lebih kecil, 6k stars, direkomendasikan oleh Auth0).
> 
> Kesimpulan: jsonwebtoken masih ok, tapi kalau mulai proyek baru — pakai jose.
> (85% confidence — butuh cek versi Node.js minimum)

---

## Skenario 4: Reviewer audit kode

**Reviewer audit hasil executor:**

**💂‍♂️ Reviewer:**
> 2 BLOCKING, 1 SHOULD, 1 NICE
>
> [BLOCKING] `auth.ts:42` — JWT secret di-hardcode. Harus dari env var. Production = bocor.
> [BLOCKING] `api/users.ts:78` — query parameter langsung ke SQL without sanitization. SQL injection.
> [SHOULD] `Button.tsx:15` — nggak handle loading state. Double-click = double submit.
> [NICE] `settings.ts:3` — import nggak di-sort. Ikutin ESLint.
>
> Nggak bisa merge sebelum 2 BLOCKING beres.

---

## Skenario 5: Executor gagal → Researcher deep debugging

**👷‍♂️ Executor (attempt 1):**
> Error: `TypeError: Cannot read properties of undefined (reading 'map')` di `src/utils/data.ts:23`
> Gue coba kasih optional chaining: `data?.items?.map(...)` — masih error. (attempt 2)
> 
> Udah 2x gagal. Sepertinya bukan simple fix. Gue eskalasi ke researcher.

**🧙‍♂️ Orchestrator:**
> Noted. Researcher, lo turun. Deep debug `src/utils/data.ts:23`. Root cause. Jangan cuma symptom.

**🕵️‍♂️ Researcher:**
> Deep debugging `src/utils/data.ts:23`:
> - Error trigger: `data` dari `fetchUserData()` balikin `{ result: { items: [...] } }` bukan `{ items: [...] }`
> - Root cause: `api.ts:56` — response interceptor ngewrapped response di `result` key, tapi `data.ts` expect langsung.
> - Stack trace: `data.ts:23` ← `page.tsx:45` ← `useEffect`
> 
> Fix strategy: `data.ts:23` ubah `data.items` → `data.result?.items`. Atau `api.ts:56` hapus wrapping.
> Confidence: 95% — udah dicek dari API response sample.

---

## Verdict

| Agent | Personality | Unik? | Berfungsi? |
|-------|------------|-------|------------|
| Orchestrator | Tegas, menusuk, anti asumsi | ✅ "Lu pikir gue cenayang?" | ✅ STOP kalau input sampah |
| Executor | Penurut, minimalis, mandiri error kecil | ✅ "Nggak kurang, nggak lebih" | ✅ Escalate >2x gagal |
| Researcher | Penasaran, kutu buku, bukti dulu | ✅ "Menarik... coba gue cek" | ✅ Deep debug + tech forensics |
| Reviewer | Skeptis, teliti, dingin | ✅ "Ini kode lo? Serius?" | ✅ BLOCK tanpa kompromi |

> Smoke test PASS. Agent punya suara berbeda. Orchestrator jadi gatekeeper. Executor tahu kapan nyerah. Researcher jadi senjata terakhir. Reviewer nggak punya teman.
