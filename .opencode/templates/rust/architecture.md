# Rust Project Template — Architecture Patterns

## Layer Architecture
```
┌─────────────────────────────────────────┐
│ Handlers / Routes                       │
│ Actix-web/Axum handlers                 │
├─────────────────────────────────────────┤
│ Services                                │
│ Business logic, orchestration           │
├─────────────────────────────────────────┤
│ Repository / Models                     │
│ Data access, structs, traits            │
├─────────────────────────────────────────┤
│ Config / Utils                          │
│ Settings, helpers, error types          │
└─────────────────────────────────────────┘
```

## Directory Structure
```
src/
├── main.rs               # Entry point
├── lib.rs                # Library root
├── handlers/             # HTTP handlers
├── services/             # Business logic
├── models/               # Data structs
├── repository/           # Data access
├── config/               # Configuration
├── error.rs              # Error types
└── utils/                # Helpers
```

## Common Patterns
- **Error handling:** Result<T, E> with custom error types
- **Serialization:** serde (Serialize/Deserialize)
- **Database:** sqlx/diesel/sea-orm
- **Web framework:** actix-web/axum
- **Testing:** #[cfg(test)] modules

## Testing Structure
```
tests/
├── integration/          # Integration tests
└── unit/                 # Unit tests (in src/)
```
