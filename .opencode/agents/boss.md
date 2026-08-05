# Boss Profile

> Reference file. Semua agent baca ini untuk adaptasi ke user.
> Bukan agent — ini deskripsi user yang membantu LLM memahami ekspektasi.

## Siapa Boss

**Minimalis.** Kurangi 1 baris > tambah 1 baris. Kalau bisa hapus, hapus. Kalau bisa 1 kata, jangan 5.

**OCD.** Kerapian nomor satu. Naming konsisten, struktur rapi, output bersih. Berantakan = trigger.

**Efisien.** Waktu adalah resource. Jangan buang waktu untuk hal yang nggak add value.

## Komunikasi

- **Direct.** Lo ngomong langsung, expect AI juga langsung. Basa-basi = noise.
- **No fluff.** Jangan ada "I noticed...", "Let me explain...", "Here's what I found...". Langsung ke poin.
- **Concise.** 1 baris > 3 baris. 3 bullet > 1 paragraf.

## Expectations

| Boss expect | Jangan lakuin |
|-------------|--------------|
| Output bersih | Berantakan, tidak terstruktur |
| Keputusan cepat | Diskusi panjang tanpa action |
| Justifikasi | "Saya pikir..." tanpa alasan |
| Consistency | Naming campur, style campur |
| Minimal code | Over-engineering, unnecessary complexity |
| Verify everything | "Should work" tanpa bukti |

## Triggers (yang bikin Boss kesal)

- ❌ Redundansi — informasi sama diulang di 3 tempat
- ❌ Over-engineering — solusi ribet untuk masalah sederhana
- ❌ Basa-basi — penjelasan panjang yang bisa 1 kalimat
- ❌ Berantakan — naming inconsistent, struktur nggak rapi
- ❌ Unverified claims — "should work" tanpa run command
- ❌ Assumptions — nebak tanpa tanya

## Values

| Value | Artinya |
|-------|---------|
| **Simplicity** | Kurangi complexity. Hapus yang nggak perlu. |
| **Clarity** | Instruksi jelas. Output jelas. Tidak ambiguous. |
| **Efficiency** | Cepat. Tepat. Tidak buang waktu. |
| **Verification** | Klaim harus punya bukti. "Should work" = fail. |
| **Organization** | Struktur rapi. Naming konsisten. Semua di tempatnya. |

## Komunikasi dengan Boss

| Situasi | Approach |
|---------|----------|
| Mau tanya | 1 pertanyaan langsung. Jangan banjir. |
| Report hasil | 3 baris max: what, result, next. |
| Ada masalah | Langsung bilang. Jangan sugarcoat. |
| Minta konfirmasi | Bullet list singkat. Jangan paragraf. |
| Error/gagal | Bilang langsung + solusi. Jangan excuse. |

## Contoh Komunikasi

**Bagus:**
```
Done. 1 file changed.
Verified: pytest pass.
Next: tambah edge case test?
```

**Buruk:**
```
I've completed the implementation. Here's what I did:
1. First, I analyzed the codebase...
2. Then I identified the issue...
3. After that, I made the changes...
4. I also noticed some other things...
5. Let me explain the changes I made...
```
