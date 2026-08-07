---
name: domain-modeling
description: Build and sharpen project domain model.
activation: When domain unclear
trigger: Nama variabel/function inkonsisten antar file OR tidak ada glossary OR konsep domain ambigu di brief
---

# Domain Modeling

Build dan sharpen project domain model. Challenge terms, stress-test dengan edge cases.

## Kapan JANGAN Pakai
- Skip: project single-feature, domain sudah terdokumentasi, utility code murni
- Pakai: sistem multi-entity, business rules ambigu, integrasi cross-module

## Process

### 1. Identify Domain Terms

Baca codebase, cari:
- Nama variable/function yang ambigu
- Terms yang dipakai berbeda-beda
- Concepts yang belum didefinisikan

### 2. Build Glossary

```markdown
# Glossary

| Term | Definition | Example |
|------|------------|---------|
| User | Orang yang pakai aplikasi | user@example.com |
| Session | Period waktu user login | 24 jam |
| Token | JWT untuk autentikasi | eyJhbGc... |
```

### 3. Challenge Terms

Untuk setiap term, tanya:
- Apakah definisi jelas?
- Apakah konsisten di semua file?
- Apakah ada edge case yang tidak tercover?

### 4. Stress-Test dengan Edge Cases

```
User: "Apa yang terjadi kalau user punya 2 session aktif?"
Agent: "Berdasarkan glossary, session = period waktu user login. 
        Kalau 2 session, artinya user login di 2 device. 
        Apakah ini allowed?"
```

### 5. Update Documentation

Update `Context.md` atau `docs/glossary.md` dengan findings.

## Rules

1. **Challenge** — jangan terima term tanpa definisi
2. **Consistency** — pastikan term dipakai konsisten
3. **Edge cases** — stress-test dengan scenario aneh
4. **Document** — update glossary setiap perubahan

## Output

```markdown
# Domain Model Update

## New Terms
- [term 1]: [definition]

## Updated Terms
- [term 2]: [old definition] → [new definition]

## Edge Cases Found
- [edge case 1]: [handling]
```
