---
name: feedback-loop
description: Learn from results and improve over time.
---

# Feedback Loop

Belajar dari hasil dan improve over time.

## Process

### 1. Record Result

Setiap task selesai, catat:
```markdown
## Result
- Task: [apa yang dilakukan]
- Status: [SUCCESS/PARTIAL/FAILURE]
- Time: [berapa lama]
- Issues: [masalah yang ditemukan]
```

### 2. Analyze Pattern

Cari pattern:
- Task type apa yang sering gagal?
- Error type apa yang sering muncul?
- Approach apa yang paling efektif?

### 3. Update Rules

Berdasarkan analysis:
- Tambah rule baru kalau pattern muncul 3x+
- Update existing rule kalau ada improvement
- Hapus rule yang tidak efektif

### 4. Apply Learning

Di task berikutnya:
- Cek apakah ada pattern yang sama
- Apply rules yang sudah diupdate
- Catat hasilnya

## Feedback Format

```markdown
# Feedback: [task name]

## What Worked
- [approach yang efektif]

## What Didn't Work
- [approach yang tidak efektif]

## Lessons Learned
- [pelajaran yang didapat]

## Rules Updated
- [rule baru atau update]
```

## Rules

1. **Record** — catat setiap hasil
2. **Analyze** — cari pattern
3. **Update** — improve rules
4. **Apply** — gunakan learning di task berikut

## Integration

- Orchestrator catat feedback setiap task selesai
- Feedback disimpan di `sub-project.md`
- Feedback dibaca di awal session baru

## Contoh

```markdown
# Feedback: Tambahin fitur login

## What Worked
- JWT implementation langsung, tidak perlu library
- Test-first approach bikin kode lebih clean

## What Didn't Work
- Rate limiting terlalu kompleks, bisa lebih simple
- Error handling terlalu verbose

## Lessons Learned
- KISS lebih penting dari feature-complete
- Test-first approach efektif untuk fitur keamanan

## Rules Updated
- Rate limiting: max 3 lines, tidak perlu library
- Error handling: 1 line per error type
```
