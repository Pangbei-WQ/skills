---
name: find-skills
description: "Discover and install skills from the open agent skills ecosystem using the Skills CLI."
---

# Find Skills

This skill helps you discover and install skills from the open agent skills ecosystem. It utilizes the Skills CLI (`npx skills`) as the package manager for modular AI agent capabilities.

## When to Use This Skill

Use this skill when:
- You need to perform a task but don't have a specialized skill for it yet.
- You want to search for tools, templates, or workflows to extend agent capabilities.
- You are looking for a specific domain-related helper (e.g., React, testing, design, deployment).
- You express interest in what other skills are available in the ecosystem.

## How to Find and Install Skills

### Step 1: Search for Skills
Run the find command with keywords related to your needs:

```powershell
npx skills find [keywords]
```

Example queries:
- `npx skills find react performance`
- `npx skills find pr review`
- `npx skills find changelog`

### Step 2: Review Options
The search will return matching skills with their repository paths and links to [skills.sh](https://skills.sh/) for more details.

### Step 3: Install a Skill
Once a relevant skill is identified, install it using the `add` command:

```powershell
npx skills add <owner/repo@skill> -g -y
```

- `-g`: Installs the skill globally (user-level).
- `-y`: Skips confirmation prompts.

## Key Skills CLI Commands

- `npx skills find [query]`: Search for skills interactively or by keyword.
- `npx skills add <package>`: Install a skill from GitHub or other sources.
- `npx skills check`: Check for updates to your installed skills.
- `npx skills update`: Update all installed skills to their latest versions.
