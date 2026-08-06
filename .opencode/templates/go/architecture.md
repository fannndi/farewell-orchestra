# Go Project Template — Architecture Patterns

## Layer Architecture
```
┌─────────────────────────────────────────┐
│ Handlers / Controllers                  │
│ HTTP handlers, middleware               │
├─────────────────────────────────────────┤
│ Services                                │
│ Business logic, orchestration           │
├─────────────────────────────────────────┤
│ Repository / Models                     │
│ Data access, structs                    │
├─────────────────────────────────────────┤
│ Config / Utils                          │
│ Settings, helpers                       │
└─────────────────────────────────────────┘
```

## Directory Structure
```
├── cmd/                  # Entry points
│   └── main.go
├── internal/             # Private packages
│   ├── handlers/         # HTTP handlers
│   ├── services/         # Business logic
│   ├── models/           # Data structs
│   ├── repository/       # Data access
│   └── middleware/       # HTTP middleware
├── pkg/                  # Public packages
├── config/               # Configuration
└── go.mod                # Dependencies
```

## Common Patterns
- **Error handling:** if err != nil { return err }
- **Serialization:** encoding/json
- **Database:** gorm/sqlx
- **Web framework:** gin/echo/fiber
- **Testing:** testing package

## Testing Structure
```
├── *_test.go             # Unit tests (in same package)
└── tests/                # Integration tests
```
