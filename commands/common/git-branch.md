---
description: Create a new git branch with conventional naming
args:
  - name: branch-name
    description: Name of the branch to create
    required: true
  - name: base-branch
    description: Base branch to branch from (default: main)
    required: false
---

# Git Branch Command

Create a new git branch following best practices.

## Instructions

You are helping the user create a new git branch. Follow these steps:

1. Check the current git status to ensure the working directory is clean
2. Fetch the latest changes from the remote
3. Checkout the base branch (default: main, or as specified by user)
4. Pull the latest changes
5. Create and checkout the new branch with the name: `{{branch-name}}`
6. Push the new branch to remote with `-u` flag to set up tracking

## Best Practices

- Use descriptive branch names that reflect the feature or fix
- Common prefixes: `feature/`, `fix/`, `chore/`, `docs/`
- Use kebab-case for branch names (e.g., `feature/add-user-auth`)
- Always verify the working directory is clean before branching

## Example

For a user request: "Create a branch for adding user authentication"

Suggested branch name: `feature/add-user-authentication`
