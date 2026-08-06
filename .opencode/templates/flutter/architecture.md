# Flutter Project Template — Architecture Patterns

## Layer Architecture
```
┌─────────────────────────────────────────┐
│ UI Layer                                │
│ Screens (full-page stateful widgets)    │
│ Widgets (reusable components)           │
├─────────────────────────────────────────┤
│ Controller Layer                        │
│ ValueNotifier / ChangeNotifier          │
│ State management (Provider/Riverpod)    │
├─────────────────────────────────────────┤
│ Service Layer                           │
│ Business logic, API calls               │
│ Platform-specific (conditional exports) │
├─────────────────────────────────────────┤
│ Data Layer                              │
│ Models (fromJson/toJson)                │
│ Storage (SharedPreferences/SQLite)      │
└─────────────────────────────────────────┘
```

## Directory Structure
```
lib/
├── main.dart                 # Entry point
├── app.dart                  # Root widget (MaterialApp)
├── models/                   # Data classes
├── screens/                  # Full-page widgets
├── services/                 # Business logic
├── utils/                    # Constants, strings, helpers
├── widgets/                  # Reusable components
└── workers/                  # Background isolates (if needed)
```

## Platform Strategy
- Conditional exports for mobile-specific code
- Stub implementations for web/desktop
- Pattern: `service.dart` exports `service_mobile.dart` or `service_stub.dart`

## State Management Options
1. **ValueNotifier** — simplest, built-in
2. **Provider** — medium complexity, good DI
3. **Riverpod** — most powerful, testable

## Testing Structure
```
test/
├── unit/                     # Model + service tests
├── widget/                   # Widget tests
├── integration/              # Full flow tests
└── golden/                   # Visual regression (optional)
```

## Common Patterns
- **Error handling:** try-catch → SnackBar for user, debugPrint for dev
- **Loading states:** bool _isLoading + CircularProgressIndicator
- **Empty states:** Icon + title + subtitle
- **Localization:** AppStrings class with language code constructor
- **Theme:** Material 3, colorSchemeSeed, dark/light modes
