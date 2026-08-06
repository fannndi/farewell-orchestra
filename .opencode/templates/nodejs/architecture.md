# Node.js Project Template — Architecture Patterns

## Layer Architecture
```
┌─────────────────────────────────────────┐
│ Routes / Controllers                    │
│ Express/Fastify routes, middleware       │
├─────────────────────────────────────────┤
│ Services                                │
│ Business logic, orchestration           │
├─────────────────────────────────────────┤
│ Models / Repositories                   │
│ Data access, ORM, schemas               │
├─────────────────────────────────────────┤
│ Utils / Config                          │
│ Helpers, constants, env config          │
└─────────────────────────────────────────┘
```

## Directory Structure
```
src/
├── index.ts              # Entry point
├── app.ts                # Express/Fastify app
├── routes/               # API routes
├── middleware/           # Auth, validation, error handling
├── services/             # Business logic
├── models/               # Data models/schemas
├── utils/                # Helpers, constants
├── config/               # Environment, database config
└── types/                # TypeScript types/interfaces
```

## Common Patterns
- **Error handling:** try-catch → error middleware → JSON response
- **Validation:** zod/joi schemas
- **Auth:** JWT middleware
- **Database:** Prisma/Drizzle/TypeORM
- **Testing:** Jest/Vitest

## Testing Structure
```
tests/
├── unit/                 # Service tests
├── integration/          # API tests
└── e2e/                  # End-to-end tests
```
