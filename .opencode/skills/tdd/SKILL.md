---
name: tdd
description: Test-driven development. Red-green-refactor loop.
activation: When writing tests
trigger: Executor writes tests
---

## Kapan JANGAN Pakai TDD
- Skip: snapshot tests, config validation, fixture data, CRUD mapping sederhana, perubahan dokumentasi
- Pakai: business logic, edge cases, security-critical code, state machine

# TDD — Test-Driven Development

Red → Green → Refactor loop. Build features atau fix bugs test-first.

## Process

### 1. Red — Tulis test yang GAGAL dulu

```python
def test_user_can_login():
    response = client.post("/login", json={"email": "test@test.com", "password": "123"})
    assert response.status_code == 200
    assert "token" in response.json()
```

Jalankan test → pastikan GAGAL.

### 2. Green — Tulis kode MINIMAL supaya test pass

```python
@app.post("/login")
def login(data: LoginData):
    return {"token": "dummy"}
```

Jalankan test → pastikan PASS.

### 3. Refactor — Bersihin kode tanpa mengubah behavior

```python
@app.post("/login")
def login(data: LoginData):
    user = authenticate(data.email, data.password)
    return {"token": create_token(user)}
```

Jalankan test → pastikan masih PASS.

## Rules

1. **Red before green** — test gagal dulu, baru tulis kode
2. **One slice at a time** — satu test, satu implementasi
3. **Minimal green** — tulis kode paling minimal yang bikin test pass
4. **Refactor after green** — bersihin kode setelah test pass

## Anti-Patterns

- ❌ Tulis semua test dulu, baru implementasi
- ❌ Test implementation detail, bukan behavior
- ❌ Skip red phase, langsung tulis kode
- ❌ Refactor di tengah red-green loop

## Contoh Flow

```
1. Tulis test: test_login_returns_token → FAIL
2. Tulis kode: /login endpoint → PASS
3. Refactor: extract authenticate() → PASS
4. Tulis test: test_login_invalid_password → FAIL
5. Tulis kode: validate password → PASS
6. Refactor: extract validate() → PASS
```
