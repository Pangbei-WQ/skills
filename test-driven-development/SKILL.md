---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code
---

# Test-Driven Development (TDD)

## The Iron Law
```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

## The RED-GREEN-REFACTOR Cycle

### 1. RED: Write a Failing Test
- Identify the smallest possible unit of work.
- Write a test and **WATCH IT FAIL**.

### 2. GREEN: Write Minimal Code
- Write the absolute minimum code to make the test pass.
- Don't care about elegance yet; hardcode if necessary to get to green fast.

### 3. REFACTOR: Clean Up
- Improve the code (names, duplication, patterns) while tests stay green.

## Rules
- Write implementation without a test? Delete it. Start over.
- Manual verification is not a substitute for automated tests.
