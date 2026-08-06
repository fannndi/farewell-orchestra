# Python Project Template — Architecture Patterns

## Layer Architecture
```
┌─────────────────────────────────────────┐
│ API Layer                               │
│ FastAPI/Flask routes, request/response   │
├─────────────────────────────────────────┤
│ Service Layer                           │
│ Business logic, orchestration           │
├─────────────────────────────────────────┤
│ Repository / Data Layer                 │
│ SQLAlchemy/Pydantic models              │
├─────────────────────────────────────────┤
│ Core / Config                           │
│ Settings, database, dependencies        │
└─────────────────────────────────────────┘
```

## Directory Structure
```
src/
├── main.py               # Entry point
├── app.py                # FastAPI/Flask app
├── api/                  # API routes
├── services/             # Business logic
├── models/               # Data models
├── schemas/              # Pydantic schemas
├── core/                 # Config, database, security
├── utils/                # Helpers
└── tests/                # Tests
```

## Common Patterns
- **Error handling:** try-catch → HTTPException → JSON response
- **Validation:** Pydantic models
- **Auth:** OAuth2/JWT
- **Database:** SQLAlchemy/Prisma
- **Testing:** pytest

## Testing Structure
```
tests/
├── unit/                 # Service tests
├── integration/          # API tests
└── conftest.py           # Fixtures
```
