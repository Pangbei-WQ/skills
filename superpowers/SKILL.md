---
name: superpowers
description: Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying questions
---

# Superpowers Skill

This skill allows the agent to automatically find and use the best available skills for any given task.

## Usage
- Run at the start of every session.
- Scan the `skills/` directory for relevant SKILL.md files.
- Before responding to any user request, identifying which skills are applicable.
- If multiple skills apply, select the most relevant ones.
- If no skills apply, proceed with standard capabilities.

## Rules
1. ALWAYS check for skills before answering.
2. If a skill exists, mention it to the User.
3. Follow the specific instructions in each skill's SKILL.md.
