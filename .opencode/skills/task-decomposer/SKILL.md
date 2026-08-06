---
name: task-decomposer
description: Break complex tasks into manageable pieces.
activation: When task is large
trigger: F=3 files
---

# Task Decomposer

Pecah task kompleks jadi bagian yang manageable.

## Process

### 1. Understand Task

Tanya:
- Apa tujuan akhirnya?
- Apa yang sudah ada?
- Apa yang perlu dibuat?
- Apa constraint-nya?

### 2. Identify Components

Pecah jadi komponen:
- **Frontend** — UI, UX, interaction
- **Backend** — API, logic, processing
- **Database** — schema, queries, migrations
- **Integration** — external services, APIs
- **Testing** — unit, integration, e2e

### 3. Create Dependency Graph

```
Component A ← Component B ← Component C
     ↓
Component D ← Component E
```

### 4. Order by Dependencies

1. Component yang tidak depend on lain
2. Component yang depend on #1
3. Component yang depend on #2
4. dst...

### 5. Create Chunks

Per chunk:
- ≤3 files
- ≤300 lines
- 1 fokus
- 1 format output

## Rules

1. **Atomic** — setiap chunk harus standalone
2. **Ordered** — urutkan berdasarkan dependencies
3. **Sized** — ≤3 files, ≤300 lines per chunk
4. **Testable** — setiap chunk bisa di-test

## Contoh

**Task:** "Bikin fitur e-commerce checkout"

**Decomposition:**
1. Cart management (frontend + backend)
2. Address form (frontend)
3. Payment integration (backend)
4. Order confirmation (frontend + backend)
5. Email notification (backend)

**Chunks:**
```
Chunk 1: Cart management
  - src/cart.ts
  - src/cart.test.ts
  - API: /api/cart

Chunk 2: Address form
  - src/address.ts
  - src/address.test.ts
  - API: /api/address

Chunk 3: Payment integration
  - src/payment.ts
  - src/payment.test.ts
  - API: /api/payment

Chunk 4: Order confirmation
  - src/order.ts
  - src/order.test.ts
  - API: /api/order

Chunk 5: Email notification
  - src/email.ts
  - src/email.test.ts
  - Service: email provider
```

## Task Priority (Eisenhower)

Prioritaskan task berdasarkan impact dan urgency.

### Priority Matrix

| | High Impact | Low Impact |
|---|---|---|
| **High Urgency** | P1 — Do First | P2 — Schedule |
| **Low Urgency** | P3 — Delegate | P4 — Drop |

### P1 — Do First
- Production bugs
- Security vulnerabilities
- Data loss risk
- Blocking other work

### P2 — Schedule
- Feature requests
- Performance improvements
- Technical debt
- Documentation

### P3 — Delegate
- Simple fixes
- Routine tasks
- Repetitive work
- Low complexity

### P4 — Drop
- Nice-to-have
- Speculative
- Low value
- High effort, low return

### Decision Tree

```
Task masuk
  │
  ▼
Apakah blocking production?
  ├── Ya → P1
  └── Tidak
        │
        ▼
      Apakah ada deadline?
        ├── Ya → P2
        └── Tidak
              │
              ▼
            Apakah complexity rendah?
              ├── Ya → P3
              └── Tidak → P4
```

### Rules

1. **Impact first** — high impact > high urgency
2. **Delegate** — low complexity → delegate ke executor
3. **Drop** — low value → drop atau defer
4. **Review** — review priority setiap session

### Integration

- Orchestrator assign priority setiap task
- Priority menentukan urutan eksekusi
- Priority bisa berubah berdasarkan context

### Contoh: Task Queue

```markdown
## Task Queue

### P1 — Do First
- [ ] Fix login bug (production down)
- [ ] Patch security vulnerability

### P2 — Schedule
- [ ] Add user dashboard
- [ ] Optimize database queries

### P3 — Delegate
- [ ] Update documentation
- [ ] Fix typo in UI

### P4 — Drop
- [ ] Add animation effects
- [ ] Refactor working code
```
