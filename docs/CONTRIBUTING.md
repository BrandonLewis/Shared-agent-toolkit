# Contributing to Shared Agent Toolkit

Thank you for your interest in contributing! This document provides guidelines and best practices for contributing to the Shared Agent Toolkit.

## How to Contribute

### 1. Report Issues

Found a bug or have a feature request?
- Check existing issues first
- Create a new issue with clear description
- Include reproduction steps for bugs
- Provide examples and use cases for features

### 2. Submit Pull Requests

#### Process
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Create a pull request

#### PR Guidelines
- **Clear title** - Summarize the change in one line
- **Description** - Explain what and why, not just how
- **Testing** - Describe how you tested the changes
- **Documentation** - Update relevant docs
- **Examples** - Include usage examples if applicable

### 3. Add Components

#### Adding a Command

```bash
# 1. Create command file in appropriate directory
touch commands/category/your-command.md

# 2. Add frontmatter and content
cat > commands/category/your-command.md << 'EOF'
---
description: Clear, concise description (50 chars max)
args:
  - name: argument-name
    description: What this argument does
    required: true
---

# Your Command Title

Clear instructions for the AI assistant...

## Instructions
Step-by-step guidance...

## Best Practices
Tips and recommendations...

## Example
Concrete usage example...
EOF

# 3. Test the command
# Install locally and test in Claude Code

# 4. Document in README if it's a major addition
```

#### Adding an Agent

```bash
# 1. Create agent definition
cat > agents/your-agent.md << 'EOF'
---
name: your-agent
description: When to invoke this agent
tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet  # Optional: haiku, sonnet, opus
---

# Agent Name

You are a specialized [role]...

## Your Responsibilities
1. Primary responsibility
2. Secondary responsibility

## Process
### Step 1: [Name]
Instructions...

### Step 2: [Name]
Instructions...

## Output Format
Expected output structure...

## Best Practices
Guidelines for this agent...

## Example
Example task and response...
EOF

# 2. Test thoroughly
# 3. Document capabilities
```

#### Adding a Skill

```bash
# 1. Create skill directory structure
mkdir -p skills/your-skill/{scripts,templates}

# 2. Create SKILL.md
cat > skills/your-skill/SKILL.md << 'EOF'
---
name: your-skill
description: What this skill does
version: 1.0.0
author: Your Name
tags: [tag1, tag2]
---

# Skill Name

Description of the skill...

## Capabilities
- Capability 1
- Capability 2

## Prerequisites
Required dependencies and setup...

## Usage Instructions
How the AI should use this skill...

## Common Patterns
Example code patterns...

## Best Practices
Guidelines...
EOF

# 3. Add helper scripts
touch skills/your-skill/scripts/helper.py
chmod +x skills/your-skill/scripts/helper.py

# 4. Add templates if needed
touch skills/your-skill/templates/template.txt

# 5. Create README
touch skills/your-skill/README.md

# 6. Test all scripts independently
python skills/your-skill/scripts/helper.py --help
```

#### Adding an MCP Server

```bash
# 1. Copy example server
cp -r mcp-servers/example-mcp mcp-servers/your-server

# 2. Customize server.py
# - Update server name
# - Add your tools
# - Implement resources and prompts
# - Add proper error handling

# 3. Update pyproject.toml
# - Change project name
# - Update description
# - Set dependencies

# 4. Create comprehensive README
# - Installation instructions
# - Configuration examples
# - Tool documentation
# - Usage examples

# 5. Test with MCP inspector
cd mcp-servers/your-server
pip install -e .
mcp-inspector python -m your_server

# 6. Test with actual AI host
# Configure in ~/.claude/mcp_settings.json
# Test all tools thoroughly
```

## Code Quality Standards

### Command Files
- ✅ Clear, actionable descriptions
- ✅ Well-structured markdown
- ✅ Proper YAML frontmatter
- ✅ Include examples
- ✅ 80 characters per line (soft limit)
- ✅ Use proper heading hierarchy

### Agent Files
- ✅ Clear role definition
- ✅ Specific, actionable instructions
- ✅ Appropriate tool restrictions
- ✅ Output format specifications
- ✅ Best practices section
- ✅ Example task/response

### Skills
- ✅ Comprehensive SKILL.md
- ✅ Executable, tested scripts
- ✅ Proper error handling in scripts
- ✅ Dependencies documented
- ✅ Type hints in Python code
- ✅ Clear docstrings

### MCP Servers
- ✅ Type-safe tool definitions
- ✅ Comprehensive error handling
- ✅ Detailed tool descriptions
- ✅ Logging for debugging
- ✅ Security considerations
- ✅ Unit tests
- ✅ Integration tests

## Testing

### Manual Testing

Before submitting:
1. Install component locally
2. Test with actual AI host
3. Verify expected behavior
4. Test edge cases
5. Check error handling

### Commands & Agents
```bash
# Install in test project
./install.sh --project --tool claude

# Test command
# In Claude Code:
/your-command test-args

# Test agent
@your-agent perform a test task
```

### Skills
```bash
# Test script independently
python skills/your-skill/scripts/helper.py --test

# Test with AI
/your-skill perform test operation
```

### MCP Servers
```bash
# Install in development mode
cd mcp-servers/your-server
pip install -e .

# Test with inspector
mcp-inspector python -m your_server

# Test each tool
# Verify all tools appear and function correctly

# Test with AI host
# Configure in mcp_settings.json
# Test in actual usage
```

## Documentation

### Required Documentation

#### Commands
- Frontmatter description
- Usage instructions
- Parameter descriptions
- Example usage

#### Agents
- Role and purpose
- When to invoke
- Expected behavior
- Output format

#### Skills
- SKILL.md with full details
- Script documentation
- Dependencies and setup
- Usage examples

#### MCP Servers
- Comprehensive README
- Installation instructions
- Configuration examples
- Tool documentation
- API reference

### Documentation Style

- **Clear and concise** - Get to the point
- **Action-oriented** - Tell users what to do
- **Examples** - Show, don't just tell
- **Troubleshooting** - Address common issues
- **Links** - Reference relevant resources

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only
- **style**: Formatting, missing semicolons, etc.
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **test**: Adding missing tests
- **chore**: Maintain, dependencies, etc.

### Examples

```
feat(commands): add code-review command

Add comprehensive code review command with security,
performance, and style checks.

Closes #42
```

```
fix(mcp): handle connection errors gracefully

Improve error handling in MCP server connection logic
to prevent crashes on network issues.

Fixes #58
```

```
docs(readme): update installation instructions

Clarify installation process and add troubleshooting
section for common issues.
```

## Code Review Process

When reviewing PRs:
- ✅ Functionality works as described
- ✅ Code follows project conventions
- ✅ Tests pass (when applicable)
- ✅ Documentation is complete
- ✅ No security issues
- ✅ Breaking changes are clearly marked

## Community Guidelines

### Be Respectful
- Treat everyone with respect
- Be constructive in feedback
- Assume good intentions
- Help newcomers

### Be Collaborative
- Discuss before major changes
- Accept feedback gracefully
- Share knowledge
- Credit others' work

### Be Professional
- Follow code of conduct
- Keep discussions on-topic
- No spam or self-promotion
- Respect maintainers' time

## Getting Help

Stuck? Need guidance?
- Check existing documentation
- Search closed issues
- Ask in discussions
- Join community Discord
- Tag maintainers for urgent issues

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Thanked in the community

Significant contributions may earn:
- Collaborator status
- Maintainer role
- Special recognition

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Shared Agent Toolkit! 🚀
