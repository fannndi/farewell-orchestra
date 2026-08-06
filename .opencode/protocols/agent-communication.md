# Agent Communication Protocol

Standard communication format between agents.

## Orchestrator → Agent Brief

```
TASK: [1 sentence — what to produce]
FILES: [path, path — files to touch]
CONTEXT: [1-2 sentences — why, constraints]
TRIED: [optional — what failed]
VERIFY: [command — how to verify completion]
CONSTRAINTS: [optional — don't change X, keep Y]
PROJECT_PATH: [absolute path — for cross-project]
PROJECT_TYPE: [Flutter/Node/Python/Rust/Go]
```

## Researcher → Orchestrator Report

```
[file]:[line] — [LEVEL] [description]

LEVEL: P (present), W (warning), E (error), O (observation)
```

Example:
```
lib/main.dart:14 — [P] unawaited(_bootstrap()) without error handler
lib/services/storage_service.dart:13 — [W] SharedPreferences not cached
```

## Reviewer → Orchestrator Report

```
[TAG] [file]:[line] — [description] — [impact]

TAG: BLOCKING, SHOULD, NICE, FYI
```

Example:
```
[BLOCKING] lib/models/github_credentials.dart:20 — Base64 not encryption — security risk
[SHOULD] lib/services/storage_service.dart:13 — SharedPreferences not cached — performance
```

## Executor → Orchestrator Report

```
Done. [X] file(s) changed.
Verified: [command output — 1 line]
```

Example:
```
Done. 5 file(s) changed.
Verified: flutter test → 12 tests passed
```

## Error Report

```
[ERROR] [type] — [description]
  Cause: [root cause]
  Fix: [solution]
  Status: [fixed/needs attention/escalated]
```

## Permission Report

```
[PERMISSION] [path] — [status]
  Action: [add to config / already configured / needs manual fix]
```
