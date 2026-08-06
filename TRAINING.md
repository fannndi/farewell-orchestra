# TRAINING.md — Prompt untuk Mengembangkan Project

> File ini berisi prompt untuk LLM guna mengembangkan Farewell Orchestra.
> Jalankan kapan saja, setiap hari, untuk optimasi berkelanjutan.
> Setiap prompt dirancang untuk menghasilkan output yang terukur.

---

## Cara Pakai

```bash
# Jalankan 1 prompt
opencode run "Baca TRAINING.md, jalankan prompt #1"

# Jalankan beberapa prompt
opencode run "Baca TRAINING.md, jalankan prompt #1 sampai #5"

# Jalankan semua prompt
opencode run "Baca TRAINING.md, jalankan semua prompt secara berurutan"

# Jalankan random
opencode run "Baca TRAINING.md, pilih 5 prompt random, jalankan"
```

---

## Level 1: Foundation (Mudah)

### Prompt #1: Audit Konsistensi
```
Baca semua file di project ini. Cek:
1. Apakah skill names di agent persona sama dengan skill folders?
2. Apakah permission di generate.py sama dengan skill yang ada?
3. Apakah README jumlah skills benar?
4. Apakah CHANGELOG terupdate?

Laporkan: X konsisten, Y inkonsisten (sebut detail).
Fix semua inkonsistensi.
```

### Prompt #2: Audit Dead Code
```
Baca semua file di project ini. Cek:
1. Apakah ada file yang tidak direferensikan oleh file lain?
2. Apakah ada import/require yang tidak dipakai?
3. Apakah ada function/variable yang tidak dipanggil?
4. Apakah ada comment yang sudah tidak relevan?

Laporkan: X dead code ditemukan. Hapus semua.
```

### Prompt #3: Audit Naming Consistency
```
Baca semua file di project ini. Cek:
1. Apakah naming convention konsisten (camelCase vs snake_case)?
2. Apakah file naming konsisten (kebab-case vs camelCase)?
3. Apakah variable naming konsisten?
4. Apakah function naming konsisten?

Laporkan: X inkonsistensi. Fix semua.
```

### Prompt #4: Audit Documentation
```
Baca semua file .md di project ini. Cek:
1. Apakah ada broken links?
2. Apakah ada outdated information?
3. Apakah ada missing documentation?
4. Apakah ada duplicate content?

Laporkan: X issues. Fix semua.
```

### Prompt #5: Audit Permissions
```
Baca opencode.jsonc dan semua agent persona. Cek:
1. Apakah permission di generate.py match dengan persona?
2. Apakah ada permission yang terlalu longgar?
3. Apakah ada permission yang terlalu ketat?
4. Apakah ada permission yang tidak dipakai?

Laporkan: X issues. Fix semua.
```

---

## Level 2: Enhancement (Sedang)

### Prompt #6: Optimize AGENTS.md
```
Baca AGENTS.md. Buat lebih:
1. Concise — hapus duplikasi
2. Clear — hapus ambiguitas
3. Complete — tambah yang kurang
4. Consistent — samakan format

Target: <100 baris, semua rules ada, tidak ada duplikasi.
```

### Prompt #7: Optimize Agent Personas
```
Baca semua agent persona (.opencode/agents/*.md). Buat lebih:
1. Identity-driven — siapa mereka, bukan apa yang mereka lakuin
2. Proaktif — jangan nunggu instruksi
3. Concise — max 50 baris per persona
4. Clear — tidak ada ambiguitas

Target: Setiap persona punya identity, rules, output format.
```

### Prompt #8: Optimize Skills
```
Baca semua skill (.opencode/skills/*/SKILL.md). Buat lebih:
1. Concise — max 50 baris per skill
2. Clear — tidak ada ambiguitas
3. Actionable — ada steps yang jelas
4. Measurable — ada success criteria

Target: Setiap skill punya purpose, steps, output format.
```

### Prompt #9: Add Missing Tests
```
Baca tests/ folder. Cek:
1. Apakah semua file punya test?
2. Apakah semua function punya test?
3. Apakah edge cases ditest?
4. Apakah error cases ditest?

Tambah test yang missing. Target: 80% coverage.
```

### Prompt #10: Add Missing Error Handling
```
Baca semua file .py dan .ts. Cek:
1. Apakah ada try-catch yang missing?
2. Apakah ada error handling yang inadequate?
3. Apakah ada error messages yang unclear?
4. Apakah ada error recovery yang missing?

Tambah error handling yang missing.
```

---

## Level 3: Advanced (Sulit)

### Prompt #11: Refactor untuk KISS
```
Baca semua file di project ini. Cek:
1. Apakah ada code yang bisa disederhanakan?
2. Apakah ada abstraction yang tidak perlu?
3. Apakah ada pattern yang over-engineered?
4. Apakah ada dependency yang tidak perlu?

Refactor untuk KISS. Target: -30% complexity.
```

### Prompt #12: Add Security Hardening
```
Baca semua file di project ini. Cek:
1. Apakah ada hardcoded secrets?
2. Apakah ada SQL injection vulnerability?
3. Apakah ada XSS vulnerability?
4. Apakah ada authentication bypass?
5. Apakah ada authorization bypass?

Fix semua security issues.
```

### Prompt #13: Add Performance Optimization
```
Baca semua file di project ini. Cek:
1. Apakah ada inefficient algorithm?
2. Apakah ada unnecessary database query?
3. Apakah ada memory leak?
4. Apakah ada slow operation?

Optimasi untuk performance.
```

### Prompt #14: Add Integration Testing
```
Buat integration test yang test:
1. Pipeline lengkap (prepare → orchestrate → implement)
2. Cross-project workflow
3. Error handling flow
4. Security flow

Target: Semua flow ter-test.
```

### Prompt #15: Add Stress Testing
```
Buat stress test yang test:
1. 50 skenario edge case
2. 50 skenario adversarial
3. 50 skenario failure
4. 50 skenario performance

Target: Semua skenario PASS.
```

---

## Level 4: Expert (Sangat Sulit)

### Prompt #16: Full System Audit
```
Audit seluruh system:
1. Architecture — apakah solid?
2. Code quality — apakah bagus?
3. Security — apakah aman?
4. Performance — apakah cepat?
5. Documentation — apakah lengkap?
6. Testing — apakah ter-test?
7. Maintainability — apakah mudah di-maintain?

Laporkan: Score 1-10 untuk setiap aspek. Rekomendasi improvement.
```

### Prompt #17: Design Pattern Analysis
```
Baca semua file di project ini. Analisis:
1. Design pattern apa yang dipakai?
2. Apakah pattern-nya benar?
3. Apakah ada pattern yang tidak perlu?
4. Apakah ada pattern yang missing?

Rekomendasi: pattern apa yang harus ditambah/dihapus.
```

### Prompt #18: Dependency Analysis
```
Baca semua file di project ini. Analisis:
1. External dependencies apa yang dipakai?
2. Apakah semua dependencies necessary?
3. Apakah ada security vulnerability di dependencies?
4. Apakah ada alternative yang lebih baik?

Rekomendasi: dependency apa yang harus ditambah/dihapus/diganti.
```

### Prompt #19: Scalability Analysis
```
Baca semua file di project ini. Analisis:
1. Apakah system bisa handle 100 concurrent users?
2. Apakah system bisa handle 1000 requests/detik?
3. Apakah system bisa handle 1GB data?
4. Apakah system bisa scale horizontally?

Rekomendasi: apa yang harus diubah untuk scalability.
```

### Prompt #20: Production Readiness
```
Audit production readiness:
1. Apakah ada monitoring?
2. Apakah ada logging?
3. Apakah ada alerting?
4. Apakah ada backup strategy?
5. Apakah ada disaster recovery?
6. Apakah ada CI/CD?
7. Apakah ada deployment strategy?

Laporkan: Score 1-10. Rekomendasi untuk production ready.
```

---

## Level 5: Innovation (Kreatif)

### Prompt #21: Add New Feature — AI-Powered Code Review
```
Buat fitur baru: AI-powered code review yang bisa:
1. Deteksi bug secara otomatis
2. Saran improvement secara otomatis
3. Security scan secara otomatis
4. Performance analysis secara otomatis

Integrasikan dengan existing system.
```

### Prompt #22: Add New Feature — Smart Documentation
```
Buat fitur baru: Smart documentation yang bisa:
1. Generate docs dari code secara otomatis
2. Update docs saat code berubah
3. Validate docs terhadap code
4. Suggest docs improvement

Integrasikan dengan existing system.
```

### Prompt #23: Add New Feature — Predictive Debugging
```
Buat fitur baru: Predictive debugging yang bisa:
1. Prediksi bug sebelum terjadi
2. Saran preventive fix
3. Monitor code quality trend
4. Alert saat quality menurun

Integrasikan dengan existing system.
```

### Prompt #24: Add New Feature — Auto-Refactoring
```
Buat fitur baru: Auto-refactoring yang bisa:
1. Deteksi code smell secara otomatis
2. Saran refactoring secara otomatis
3. Execute refactoring dengan safety check
4. Validate refactoring tidak break existing functionality

Integrasikan dengan existing system.
```

### Prompt #25: Add New Feature — Performance Monitoring
```
Buat fitur baru: Performance monitoring yang bisa:
1. Monitor response time
2. Monitor memory usage
3. Monitor CPU usage
4. Monitor error rate
5. Alert saat performance menurun

Integrasikan dengan existing system.
```

---

## Daily Training Routine

### Pagi (15 menit)
```bash
opencode run "Baca TRAINING.md, jalankan prompt #1 sampai #5"
```

### Siang (30 menit)
```bash
opencode run "Baca TRAINING.md, jalankan prompt #6 sampai #10"
```

### Malam (60 menit)
```bash
opencode run "Baca TRAINING.md, jalankan prompt #11 sampai #15"
```

### Weekend (2 jam)
```bash
opencode run "Baca TRAINING.md, jalankan prompt #16 sampai #25"
```

---

## Metrics Tracking

Setelah setiap training, catat:

```markdown
## Training Log: [tanggal]

### Prompt yang Dijalankan: #[nomor]
### Issues Ditemukan: [jumlah]
### Issues Fixed: [jumlah]
### Time Taken: [durasi]
### Token Used: [estimasi]

### Improvements:
- [improvement 1]
- [improvement 2]

### Next Steps:
- [next step 1]
- [next step 2]
```

---

## Success Criteria

| Level | Target | Timeframe |
|-------|--------|-----------|
| Level 1 | 0 issues | 1 minggu |
| Level 2 | 0 issues | 2 minggu |
| Level 3 | 0 issues | 1 bulan |
| Level 4 | Score 8+/10 | 2 bulan |
| Level 5 | 5 features | 3 bulan |

---

## Notes

- **Jangan skip level** — selesaikan level 1 dulu sebelum level 2
- **Catat semua** — setiap training harus dicatat
- **Iterate** — kalau ada issue baru, tambah ke prompt
- **Measure** — ukur improvement setiap training
- **Report** — lapor hasil training ke Boss
