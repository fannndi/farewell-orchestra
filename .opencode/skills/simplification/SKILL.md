---
name: simplification
description: Guide untuk menyederhanakan kode yang sudah ada.
activation: When code is complex
trigger: Reviewer flags complexity
---

# Simplification Guide

Cara menyederhanakan kode yang sudah ada.

## Principle

> "Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away." — Antoine de Saint-Exupéry

## Step 1: Identify Complexity

Tanya:
- Ada file yang tidak perlu?
- Ada abstraction yang tidak perlu?
- Ada pattern yang tidak perlu?
- Ada dependency yang tidak perlu?
- Ada kode yang tidak dipakai?

## Step 2: Merge Files

**Kalau file < 100 baris dan logic sama → gabung**

Before:
```
src/utils/string.ts (20 baris)
src/utils/number.ts (15 baris)
src/utils/date.ts (25 baris)
```

After:
```
src/utils.ts (60 baris)
```

## Step 3: Remove Abstractions

**Kalau abstraction dipakai 1x → hapus**

Before:
```typescript
interface UserService {
  getUser(id: string): User;
}

class UserServiceImpl implements UserService {
  getUser(id: string): User { ... }
}
```

After:
```typescript
function getUser(id: string): User { ... }
```

## Step 4: Remove Patterns

**Kalau pattern tidak perlu → hapus**

Before:
```typescript
class UserFactory {
  create(data: UserData): User {
    return new User(data);
  }
}
```

After:
```typescript
const user = new User(data);
```

## Step 5: Remove Dependencies

**Kalau dependency bisa diganti stdlib → hapus**

Before:
```typescript
import { v4 as uuid } from 'uuid';
const id = uuid();
```

After:
```typescript
const id = crypto.randomUUID();
```

## Step 6: Simplify Logic

**Kalau logic bisa lebih sederhana → sederhanakan**

Before:
```typescript
const result = condition1
  ? condition2
    ? value1
    : value2
  : condition3
    ? value3
    : value4;
```

After:
```typescript
let result;
if (condition1 && condition2) result = value1;
else if (condition1) result = value2;
else if (condition3) result = value3;
else result = value4;
```

## Step 7: Remove Dead Code

**Kalau kode tidak dipakai → hapus**

- Unused imports
- Unused functions
- Unused variables
- Commented code
- TODO/FIXME yang sudah tidak relevan

## Metrics

| Metric | Target |
|--------|--------|
| Files per feature | ≤ 3 |
| Lines per file | ≤ 300 |
| Functions per file | ≤ 10 |
| Dependencies per project | ≤ 20 |
| Abstraction layers | ≤ 2 |

## Contoh: Simplification Process

### Step 0: Original (245 baris, 7 file)
```
src/auth/auth.controller.ts (50)
src/auth/auth.service.ts (80)
src/auth/auth.middleware.ts (30)
src/auth/auth.validator.ts (20)
src/auth/auth.types.ts (15)
src/auth/auth.repository.ts (40)
src/auth/auth.config.ts (10)
```

### Step 1: Identify
- auth.types.ts (15 baris) → bisa digabung
- auth.config.ts (10 baris) → bisa digabung
- auth.validator.ts (20 baris) → bisa digabung

### Step 2: Merge
```
src/auth/auth.controller.ts (50)
src/auth/auth.service.ts (80 + 15 + 10 + 20 = 125)
src/auth/auth.middleware.ts (30)
src/auth/auth.repository.ts (40)
```

### Step 3: Remove middleware
- auth.middleware.ts (30 baris) → bisa digabung ke controller

### Step 4: Final
```
src/auth.ts (150 baris)
```

### Result
- **Before:** 7 file, 245 baris
- **After:** 1 file, 150 baris
- **Penghematan:** 6 file, 95 baris (39%)
