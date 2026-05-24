---
name: using-git-worktrees
description: Use when you need to work on multiple branches simultaneously or isolate environment state.
---

# Using Git Worktrees

## Core Principle
One task = One directory.

## Usage
- **Parallel Tasks**: Work on a feature while fixing a critical bug in a separate directory.
- **Task Isolation**: Keep environment state (node_modules, build artifacts) separate between branches.

## Workflow
1. **Create**: `git worktree add ../branch-name branch-to-checkout`
2. **Work**: Use separate editor instances for each directory.
3. **Cleanup**: Once merged, remove the directory using `git worktree remove`.

## Mistakes to Avoid
- Don't create nested worktrees.
- Always use `../` to keep worktrees alongside your main repo.
