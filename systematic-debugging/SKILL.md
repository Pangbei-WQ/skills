---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
---

# Systematic Debugging

## Overview
Random fixes waste time and create new bugs. Quick patches mask underlying issues. **Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

## The Iron Law
```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

## The Four Phases

### Phase 1: Root Cause Investigation
**BEFORE attempting ANY fix:**
1. **Read Error Messages Carefully**: Read stack traces completely, note line numbers and file paths.
2. **Reproduce Consistently**: Identify the exact steps to trigger the issue reliably.
3. **Gather Evidence**: Add diagnostic instrumentation/logging to identify WHERE it breaks in multi-component systems.
4. **Trace Data Flow**: Trace bad values back to their origin.

### Phase 2: Pattern Analysis
1. **Find Working Examples**: Compare broken code against similar working code in the same codebase.
2. **Compare Against References**: Read reference implementations completely.
3. **Identify Differences**: List every difference, however small.

### Phase 3: Hypothesis and Testing
1. **Form Single Hypothesis**: State clearly: "I think X is the root cause because Y."
2. **Test Minimally**: Make the smallest possible change to test the hypothesis (one variable at a time).
3. **Verify**: If it didn't work, form a NEW hypothesis. Don't add more fixes on top.

### Phase 4: Implementation
1. **Create Failing Test Case**: Use TDD to write a failing test that reproduces the bug.
2. **Implement Single Fix**: Address the identified root cause.
3. **Verify Fix**: Ensure the test now passes and no regressions were introduced.
4. **Question Architecture**: If 3+ fixes failed, stop and discuss if the underlying pattern is flawed.
