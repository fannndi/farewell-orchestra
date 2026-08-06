---
name: anti-patterns
description: Database of over-engineering patterns. Flag kalau nemu.
activation: When reviewing code
trigger: Reviewer finds complexity
---

# Anti-Patterns Database

Pattern yang harus di-flag kalau ditemukan di output.

## File Organization

| Pattern | Severity | Contoh | Solusi |
|---------|----------|--------|--------|
| Fitur kecil, 5+ file | SHOULD | auth.controller.ts, auth.service.ts, auth.middleware.ts, auth.validator.ts, auth.types.ts | Gabung jadi 1 file |
| File kosong/hampir kosong | SHOULD | auth.types.ts (cuma 5 baris) | Gabung ke file utama |
| Naming terlalu panjang | NICE | getUserDataFromDatabaseByUserId | getData(userId) |
| Folder terlalu dalam | NICE | src/modules/auth/services/impl/v2/ | src/auth/ |

## Code Patterns

| Pattern | Severity | Contoh | Solusi |
|---------|----------|--------|--------|
| Abstract class, 1 implementasi | SHOULD | abstract class BaseAuth { } class Auth extends BaseAuth { } | Hapus abstract class |
| Factory, 1 objek | SHOULD | class AuthFactory { create() { return new Auth(); } } | new Auth() langsung |
| Strategy, 1 strategi | SHOULD | interface Strategy { execute(); } class ConcreteStrategy implements Strategy { } | Tulis langsung |
| Observer, 1 event | SHOULD | class EventBus { on() {} emit() {} } | Callback langsung |
| Builder, 5 field | SHOULD | new UserBuilder().setName().setEmail().setAge().setPhone().setAddress().build() | new User({name, email, age, phone, address}) |
| Middleware chain | SHOULD | app.use(auth).use(validate).use(transform).use(log) | Gabung jadi 1 middleware |

## Dependencies

| Pattern | Severity | Contoh | Solusi |
|---------|----------|--------|--------|
| Dependency untuk 1 fungsi | SHOULD | import { formatDate } from 'date-fns' (cuma dipakai 1x) | Intl.DateTimeFormat atau tulis sendiri |
| Dependency yang bisa stdlib | SHOULD | import { uuid } from 'uuid' | crypto.randomUUID() |
| Dependency yang bisa 10 baris | SHOULD | import { slugify } from 'slugify' | function slugify(s) { return s.toLowerCase().replace(/\s+/g, '-'); } |
| Multiple dependency yang mirip | SHOULD | lodash + underscore + ramda | Pilih 1 |

## Abstraction

| Pattern | Severity | Contoh | Solusi |
|---------|----------|--------|--------|
| Interface untuk 1 implementasi | SHOULD | interface UserService { } class UserServiceImpl implements UserService { } | Hapus interface |
| Generic yang tidak perlu | SHOULD | class Repository<T extends Entity> { } | class Repository { } |
| Decorator pattern | SHOULD | @Log @Cache @Validate @Transform | Tulis langsung |
| Mixin pattern | SHOULD | class User extends withTimestamps(withSoftDelete(Base)) { } | Tulis langsung |

## Complexity

| Pattern | Severity | Contoh | Solusi |
|---------|----------|--------|--------|
| Nested ternary | SHOULD | a ? b ? c : d : e | if-else |
| Chained optional | NICE | a?.b?.c?.d?.e | if (a && a.b && a.b.c) |
| Complex regex | SHOULD | /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/ | Pisah jadi beberapa check |
| Magic numbers | NICE | if (status === 3) | if (status === STATUS_ACTIVE) |

## Testing

| Pattern | Severity | Contoh | Solusi |
|---------|----------|--------|--------|
| Test terlalu banyak mock | SHOULD | mock everything, test nothing real | Test integrasi |
| Test terlalu detail | NICE | test implementation detail | Test behavior |
| Test yang tidak perlu | NICE | test getter/setter | Hapus |

## Contoh: Before vs After

### Before (Over-Engineered)
```
src/
  auth/
    auth.controller.ts (50 baris)
    auth.service.ts (80 baris)
    auth.middleware.ts (30 baris)
    auth.validator.ts (20 baris)
    auth.types.ts (15 baris)
    auth.repository.ts (40 baris)
    auth.config.ts (10 baris)
```
Total: 7 file, 245 baris

### After (KISS)
```
src/
  auth.ts (150 baris)
```
Total: 1 file, 150 baris

**Penghematan:** 6 file, 95 baris
