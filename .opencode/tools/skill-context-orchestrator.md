# Auto-loaded Skills for orchestrator

This file is auto-generated. Do not edit manually.

=== SKILL: prepare ===
---
name: prepare
description: Use when receiving a request — validate input, extract requirements, chunk if needed. Gate before orchestration.
---

# Prepare

Gate awal sebelum dispatch. Flow:

```
Request → Cross-Project? → YES → Check Docs → Reverse Engineer? → Generate → Normal Flow
                ↓ NO
         Input Validation → HOLD? STOP. PARTIAL? → Grill. PASS? → Chunk → Dispatch
```

## Fallback Mode (untuk semua LLM)

=== SKILL: orchestrate ===
---
name: orchestrate
description: Use after prepare passes — decompose, fan-out parallel, synthesize, brief executor.
---

# Orchestrate

Input sudah CLEAN. Flow:

```
Decompose → Evidence Bundle → Ping → Fan-Out → Synthesize → Verify Gate → Brief Executor → Post-Flight
```

## Fallback Mode (untuk semua LLM)

=== SKILL: kiss-checklist ===
---
name: kiss-checklist
description: Pre-implementation checklist. WAJIB sebelum nulis kode.
---

# KISS Checklist

WAJIB sebelum nulis kode. Cek semua.

## Pre-Implementation

=== SKILL: complexity-budget ===
---
name: complexity-budget
description: Limit complexity per feature. Kalau melebihi, pecah atau sederhanakan.
---

# Complexity Budget

Limit complexity per feature. Kalau melebihi, pecah atau sederhanakan.

## Budget Per Feature

=== SKILL: progress-tracker ===
---
name: progress-tracker
description: Persistent task tracking. Track progress across sessions.
---

# Progress Tracker

Persistent task tracking. Track progress across sessions.

## Format

=== SKILL: error-handler ===
---
name: error-handler
description: Error classification + recovery. Handle errors differently based on type.
---

# Error Handler

Error classification + recovery. Handle errors differently based on type.

## Error Classification

=== SKILL: context-manager ===
---
name: context-manager
description: Context prioritization. Manage context across sessions.
---

# Context Manager

Context prioritization. Manage context across sessions.

## Context Priority