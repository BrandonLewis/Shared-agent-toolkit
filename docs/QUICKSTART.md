# Quick Start Guide

Get up and running with the Shared Agent Toolkit in 5 minutes.

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/shared-agent-toolkit.git
cd shared-agent-toolkit
```

### Step 2: Install for Your Tool

**For Claude Code:**
```bash
./install.sh --global --tool claude
```

**For Cursor:**
```bash
./install.sh --global --tool cursor
```

**For a specific project:**
```bash
cd /path/to/your/project
/path/to/shared-agent-toolkit/install.sh --project --tool claude
```

### Step 3: Restart Your AI Host

Close and reopen Claude Code, Cursor, or your AI coding assistant.

## Your First Command

### Try a Built-in Command

In Claude Code, try:
```
/git-branch my-feature
```

This will:
1. Check git status
2. Fetch latest changes
3. Create and checkout a new branch
4. Push to remote with tracking

### Review Some Code

```
/review --focus security
```

The AI will:
1. Review recent changes
2. Focus on security issues
3. Provide detailed feedback
4. Suggest improvements

## Your First Agent

Agents are invoked by asking the AI to use them or with `@agent-name`:

```
@code-reviewer please review the changes in auth.py for security issues
```

The code-reviewer agent will:
1. Read auth.py
2. Analyze for security vulnerabilities
3. Check for best practices
4. Provide actionable feedback

## Your First Skill

Skills bundle prompts with executable scripts:

```
/excel-automation read data from quarterly_report.xlsx
```

The excel-automation skill will:
1. Execute the appropriate script
2. Read the Excel file
3. Extract data
4. Present formatted results

## Create Your First Custom Command

### Simple Command

```bash
# Create a new command file
cat > ~/.claude/commands/hello.md << 'EOF'
---
description: Say hello in a friendly way
---

# Hello Command

Greet the user warmly and ask how you can help them today.
EOF
```

Now use it:
```
/hello
```

### Command with Arguments

```bash
cat > ~/.claude/commands/summarize.md << 'EOF'
---
description: Summarize a file
args:
  - name: file-path
    description: Path to file to summarize
    required: true
---

# Summarize File

Read the file at `{{file-path}}` and provide:
1. A one-sentence summary
2. Key points (3-5 bullet points)
3. Any notable observations
EOF
```

Use it:
```
/summarize README.md
```

## Create Your First Agent

```bash
cat > ~/.claude/agents/writer.md << 'EOF'
---
name: writer
description: Technical writing and documentation
tools: Read, Write, Glob
model: sonnet
---

# Technical Writer Agent

You are an expert technical writer specializing in clear,
concise documentation.

## Your Responsibilities
1. Write clear, user-focused documentation
2. Follow documentation best practices
3. Use proper markdown formatting
4. Include examples where helpful

## Style Guide
- Active voice
- Short sentences
- Concrete examples
- Logical structure
- Proper headings

## Process
1. Understand the topic
2. Identify the audience
3. Create outline
4. Write content
5. Review for clarity
EOF
```

Use it:
```
@writer help me document this API endpoint
```

## Create Your First Skill

### Directory Structure

```bash
mkdir -p ~/.claude/skills/hello-skill/scripts
```

### SKILL.md

```bash
cat > ~/.claude/skills/hello-skill/SKILL.md << 'EOF'
---
name: hello-skill
description: Example skill with a script
version: 1.0.0
---

# Hello Skill

This skill demonstrates how to bundle a prompt with a script.

## Usage

When the user invokes this skill, execute the hello.py script
and present the output in a friendly way.
EOF
```

### Script

```bash
cat > ~/.claude/skills/hello-skill/scripts/hello.py << 'EOF'
#!/usr/bin/env python3
import sys
from datetime import datetime

name = sys.argv[1] if len(sys.argv) > 1 else "there"
time = datetime.now().strftime("%I:%M %p")

print(f"Hello, {name}!")
print(f"The current time is {time}")
print("Have a great day!")
EOF

chmod +x ~/.claude/skills/hello-skill/scripts/hello.py
```

### Use It

```
/hello-skill
```

## Working with MCP Servers

### Install Example Server

```bash
cd shared-agent-toolkit/mcp-servers/example-mcp
pip install -e .
```

### Configure Claude Code

Edit `~/.claude/mcp_settings.json`:

```json
{
  "mcpServers": {
    "example": {
      "command": "python",
      "args": ["-m", "example_mcp"]
    }
  }
}
```

### Restart Claude Code

The MCP server will load automatically.

### Use MCP Tools

Just ask the AI naturally:

```
Can you use the example MCP to calculate the sum of 42 and 58?
```

The AI will automatically use the `calculate_sum` tool from the MCP server.

## Common Workflows

### Development Workflow

```bash
# 1. Create feature branch
/git-branch feature/new-feature

# 2. Make changes
# ... edit code ...

# 3. Review changes
/review --focus all

# 4. Commit (manually or with commit skill)
git add .
git commit -m "Add new feature"
git push
```

### Research Workflow

```bash
# Ask research agent
@research-agent what are the best practices for API rate limiting in Node.js?

# The agent will:
# - Search documentation
# - Review code patterns
# - Provide recommendations
# - Include sources
```

### Data Processing Workflow

```bash
# Extract from PDF
/pdf-extraction extract tables from report.pdf

# Process with Excel
/excel-automation analyze the extracted data

# Generate report
@writer create a summary report of the findings
```

## Tips and Tricks

### Combining Commands

Commands can reference each other:

```
First, /review the code, then if it looks good, help me /git-branch a release branch
```

### Agent Delegation

The main AI can delegate to multiple agents:

```
Please have @research-agent find the best approach, then @code-reviewer validate the implementation
```

### Skill + Agent

Use skills for execution, agents for intelligence:

```
/excel-automation extract the data, then @writer create documentation
```

### MCP + Commands

MCP provides data, commands provide workflow:

```
Use the construction MCP to query historical pricing, then help me /bid-analysis
```

## Troubleshooting

### Command Not Found

```bash
# Check if installed
ls ~/.claude/commands/

# Reinstall
./install.sh --global --tool claude

# Restart Claude Code
```

### Agent Not Loading

```bash
# Verify file exists
cat ~/.claude/agents/your-agent.md

# Check syntax (frontmatter format)
# Restart Claude Code
```

### Skill Script Error

```bash
# Test script independently
python ~/.claude/skills/your-skill/scripts/script.py

# Check permissions
chmod +x ~/.claude/skills/your-skill/scripts/script.py

# Verify Python dependencies
pip list
```

### MCP Server Not Connecting

```bash
# Test server
python -m your_mcp_server

# Check configuration
cat ~/.claude/mcp_settings.json

# Verify installation
pip list | grep mcp

# Check logs
# Claude Code shows MCP connection status
```

## Next Steps

1. **Explore Examples**
   - Try all included commands
   - Test agents with various tasks
   - Use skills for real work

2. **Customize**
   - Modify commands for your workflow
   - Create domain-specific agents
   - Build skills for your common tasks

3. **Build**
   - Create commands for your projects
   - Develop agents for your domain
   - Build MCP servers for your integrations

4. **Share**
   - Contribute back to the repository
   - Share with your team
   - Help improve documentation

## Resources

- [Full Documentation](../README.md)
- [Architecture Guide](ARCHITECTURE.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Claude Code Docs](https://code.claude.com/docs)
- [MCP Documentation](https://modelcontextprotocol.io/)

## Getting Help

- Check [README.md](../README.md) for detailed docs
- Review examples in repository
- Search [GitHub Issues](https://github.com/yourusername/shared-agent-toolkit/issues)
- Ask in discussions
- Join community Discord

---

**Happy coding with AI! 🚀**
