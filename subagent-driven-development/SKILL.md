---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session
---

# Subagent-Driven Development (SDD) Skill

This skill is for executing complex implementation plans by delegating tasks to specialized subagents. It emphasizes clear roles, rigorous review, and error handling.

## Roles
- **Orchestrator (Main Agent)**: Decides which subagents to launch and integrates their work.
- **Implementer (Subagent)**: Performs the actual coding or research based on instructions.
- **Spec-Reviewer (Subagent)**: Checks the work against the original requirements and technical specifications.
- **Quality-Reviewer (Subagent)**: Checks for code quality, naming conventions, and project standards.

## Workflow
1. **Task Extraction**: Identify task blocks from the implementation plan.
2. **Context Preparation**: Gather all necessary file paths, context files, and requirements for the specific task.
3. **Launch Implementer**: Dispatch a subagent with clear, detailed instructions and a specific goal.
4. **Review Cycle**:
    - Implementer reports completion.
    - (Optional) Launch a Reviewer subagent to verify the Implementer's work.
    - Implementer addresses any review findings.
5. **Integration**: Main agent verifies and integrates the subagent's work into the project.
6. **Status Update**: Update the master implementation plan's status.

## Error Handling
- If a subagent encounters a blocker, the main agent must resolve it or adjust the plan.
- If work fails review, it must be iterated upon until it passes.
