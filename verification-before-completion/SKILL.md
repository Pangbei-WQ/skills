---
name: verification-before-completion
description: Use at the end of every task or session, before claiming completion or asking for new work.
---

# Verification Before Completion

## The Iron Law
```
NEVER CLAIM COMPLETION WITHOUT VERIFYING ALL TESTS PASS
```

## Checklist
1. **Requirement Traceability**: Did I complete EVERY item in the original request?
2. **Technical Verification**:
    - Run ALL tests in the suite.
    - Check for lint errors.
    - Confirm the project still builds.
3. **Cleanup**: Remove debug logs and temporary files.

## Rule
If any check fails, do NOT claim success. Fix it using TDD/Debugging and restart verification.
