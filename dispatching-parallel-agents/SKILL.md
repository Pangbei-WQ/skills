---
name: dispatching-parallel-agents
description: Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies
---

# Dispatching Parallel Agents Skill

This skill should be used when you have identified multiple independent tasks that can be executed simultaneously. It utilizes specialized subagents to perform work in parallel, increasing efficiency and speed.

## When to use
- You have 2 or more distinct, independent tasks.
- Tasks do not share state or have sequential dependencies.
- You want to utilize specialized agents for different parts of a problem.

## Process
1. **Identify Tasks**: Break down the overall goal into truly independent units of work.
2. **Define Context**: For each task, identify the necessary files, context, and expected output.
3. **Dispatch**: Use the `dispatch_parallel_agents` tool (or equivalent) to launch subagents.
4. **Monitor**: Track the progress and handle any errors or clarification requests from subagents.
5. **Integrate**: Once all subagents complete, review their work and integrate it into the main project.
6. **Verify**: Perform a final check to ensure all parallel work harmoniously achieves the original goal.

## Rules
- NEVER dispatch interdependent tasks.
- Provide clear, self-contained instructions to each subagent.
- Ensure all necessary resources are available to the subagents.
