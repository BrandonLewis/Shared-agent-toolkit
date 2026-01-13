# Shared Agent Toolkit

A comprehensive, portable repository of AI agent components including slash commands, subagents, skills, and MCP servers that work across multiple AI coding assistants.

## Overview

This toolkit provides reusable, version-controlled agent components that can be shared across projects and teams. It follows emerging best practices from the agentic coding ecosystem and is compatible with:

- **Claude Code** - Full support for commands, agents, skills, and MCP servers
- **Cursor** - Compatible rules and context
- **Aider** - Command integration (experimental)
- **Any MCP-compatible host** - Universal MCP server support

## Repository Structure

```
shared-agent-toolkit/
├── commands/               # Slash commands (portable markdown)
│   ├── construction/       # Domain-specific commands
│   ├── dev/               # Development commands
│   └── common/            # Common utilities
│
├── agents/                # Subagent definitions
│   ├── code-reviewer.md   # Code review specialist
│   ├── research-agent.md  # Research and analysis
│   └── estimator-agent.md # Construction estimator
│
├── skills/                # Bundled skills with scripts
│   ├── excel-automation/  # Excel processing
│   ├── pdf-extraction/    # PDF text and table extraction
│   └── bid-processing/    # Construction bid processing
│
├── mcp-servers/           # MCP server implementations
│   ├── example-mcp/       # Basic example server
│   └── construction-toolkit/ # Construction industry tools
│
├── hooks/                 # Event hooks (Claude Code)
├── adapters/              # Cross-tool compatibility
├── docs/                  # Additional documentation
└── install.sh            # Installation script
```

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/shared-agent-toolkit.git
cd shared-agent-toolkit

# Install globally for Claude Code
./install.sh --global --tool claude

# Or install in current project
./install.sh --project --tool claude

# For other tools
./install.sh --global --tool cursor
./install.sh --global --tool aider
```

### Using Commands

Commands are invoked with `/` prefix:

```
/git-branch feature-name
/review --focus security
/takeoff spec.pdf --unit TON
```

### Using Agents

Reference agents with `@` or invoke directly:

```
@code-reviewer please review the authentication changes
@research-agent what are the current best practices for rate limiting?
@estimator-agent analyze this bid tabulation
```

### Using Skills

Skills are invoked like commands but bundle additional scripts and resources:

```
/excel-automation extract data from quarterly_report.xlsx
/pdf-extraction extract tables from bid_tab.pdf
```

## Components

### 1. Commands

Slash commands are markdown files with optional YAML frontmatter that provide reusable prompts and workflows.

**Format:**
```markdown
---
description: Command description
args:
  - name: argument-name
    description: What this argument does
    required: true/false
---

# Command Title

Command instructions for the AI...
```

**Example Commands:**
- `/git-branch` - Create git branches with best practices
- `/review` - Comprehensive code review
- `/takeoff` - Construction quantity takeoffs

**Creating Your Own:**
```bash
# Add a new command
touch commands/mycommand.md
# Edit with your prompt and frontmatter
```

### 2. Agents (Subagents)

Agents are specialized AI assistants with specific expertise and tools. They operate with isolated context to maintain focus.

**Format:**
```markdown
---
name: agent-name
description: When to use this agent
tools: Read, Write, Edit, Bash, Grep, Glob
model: sonnet  # optional
---

# Agent Role

You are a [specialized role]...

## Responsibilities
...

## Process
...
```

**Key Architectural Insight:**

Subagents have separate context windows from the main agent. This prevents "implementation noise" from cluttering the orchestration layer. The main agent stays in pure orchestration mode while subagents handle detailed implementation.

**Example Agents:**
- **code-reviewer** - Security, performance, and quality review
- **research-agent** - Information gathering and synthesis
- **estimator-agent** - Construction cost estimation

### 3. Skills

Skills are enhanced commands that bundle prompts with scripts, templates, and supporting resources.

**Structure:**
```
skills/skill-name/
├── SKILL.md          # Main instructions
├── scripts/          # Helper scripts
│   └── helper.py
├── templates/        # File templates
└── README.md         # Documentation
```

**Advantages over MCP:**
- Don't consume context window upfront
- Only loaded when invoked
- Can bundle domain-specific documentation
- Easier to maintain and version control

**Example Skills:**
- **excel-automation** - Read, write, format Excel files
- **pdf-extraction** - Extract text and tables from PDFs
- **bid-processing** - Construction bid workflows

### 4. MCP Servers

MCP (Model Context Protocol) servers provide standardized tool integration across AI hosts.

**Architecture:**
```
AI Host (Claude Code, etc.)
    ↓
MCP Client
    ↓
MCP Server
    ↓
Your Data/Tools/APIs
```

**Key Insight:**

MCP is not an agent framework—it's a standardized integration layer. One MCP server works across Claude Code, Claude Desktop, Cursor, OpenAI Agents SDK, and any other MCP-compatible host.

**Example Servers:**
- **example-mcp** - Template for creating new servers
- **construction-toolkit** - HeavyBid, Procore, CALTRANS integration

**Installing an MCP Server:**
```bash
cd mcp-servers/construction-toolkit
pip install -e .

# Configure in ~/.claude/mcp_settings.json
{
  "mcpServers": {
    "construction": {
      "command": "python",
      "args": ["-m", "construction_toolkit"],
      "env": {
        "HEAVYBID_DB_PATH": "/path/to/database"
      }
    }
  }
}
```

## Architecture Patterns

### Command Pattern

Commands follow a simple markdown + frontmatter pattern:
- **Portable** - Work across different AI tools
- **Versionable** - Standard text files in git
- **Discoverable** - Directory structure creates namespaces
- **Composable** - Commands can invoke other commands

### Agent Pattern

Agents follow the "orchestrator-worker" pattern:
- **Main agent** orchestrates and delegates
- **Sub-agents** execute with focused context
- **Isolated context** prevents cross-contamination
- **Tool restrictions** limit agent capabilities appropriately

### Skill Pattern

Skills bundle related capabilities:
- **Prompt + Code** - Instructions plus executable scripts
- **On-demand loading** - Don't consume context until invoked
- **Self-contained** - All dependencies bundled together
- **Domain-specific** - Tailored for particular use cases

### MCP Pattern

MCP servers provide universal tool integration:
- **One server, many hosts** - Write once, use everywhere
- **Standardized protocol** - Interoperable across vendors
- **Async operations** - Supports long-running tasks
- **Type-safe** - Strong typing for tools and parameters

## Cross-Tool Compatibility

### Claude Code
✅ **Full Support**
- Commands: `.claude/commands/`
- Agents: `.claude/agents/`
- Skills: `.claude/skills/`
- MCP: `~/.claude/mcp_settings.json`
- Hooks: `.claude/hooks/`

### Cursor
⚠️ **Partial Support**
- Rules: `.cursor/rules/` (use adapter)
- Limited agent support
- MCP support available

### Aider
⚠️ **Experimental**
- Custom commands via `.aider/`
- Limited integration

### Using the Adapter

For tools that use different formats:

```bash
# Convert commands to Cursor rules
python adapters/cursor_adapter.py \
  --input commands/ \
  --output ~/.cursor/rules/shared/
```

## Creating Your Own Components

### New Command

```bash
# Create file
touch commands/mycategory/mycommand.md

# Add content
cat > commands/mycategory/mycommand.md << 'EOF'
---
description: What this command does
---

# My Command

Instructions for the AI...
EOF
```

### New Agent

```bash
# Create agent definition
cat > agents/my-agent.md << 'EOF'
---
name: my-agent
description: When to use this agent
tools: Read, Write, Grep
---

# My Specialized Agent

You are an expert in...
EOF
```

### New Skill

```bash
# Create skill directory
mkdir -p skills/my-skill/scripts

# Create SKILL.md
touch skills/my-skill/SKILL.md

# Add helper scripts
touch skills/my-skill/scripts/helper.py
```

### New MCP Server

```bash
# Copy template
cp -r mcp-servers/example-mcp mcp-servers/my-server

# Customize server.py
# Update pyproject.toml
# Add your tools and logic
```

## Best Practices

### Version Control
- ✅ Commit all changes to git
- ✅ Use semantic versioning for releases
- ✅ Tag stable versions
- ✅ Document breaking changes

### Organization
- ✅ Use clear, descriptive names
- ✅ Group related commands in directories
- ✅ Maintain consistent structure
- ✅ Document all components

### Testing
- ✅ Test commands before committing
- ✅ Validate agent behavior
- ✅ Test skill scripts independently
- ✅ Use MCP inspector for servers

### Documentation
- ✅ Write clear descriptions
- ✅ Provide usage examples
- ✅ Document parameters and options
- ✅ Explain the "why" not just the "what"

### Security
- ⚠️ Never commit API keys or secrets
- ⚠️ Review file access permissions
- ⚠️ Validate all inputs
- ⚠️ Use environment variables for sensitive config

## Examples

### Construction Workflow

```bash
# 1. Extract bid items from PDF
/pdf-extraction extract tables from bid_tab.pdf

# 2. Analyze the bid
@estimator-agent analyze bid_items.xlsx for completeness

# 3. Calculate quantities
/takeoff specifications.pdf --unit CY

# 4. Query historical pricing (via MCP)
# Agent automatically uses construction-toolkit MCP server
# to query HeavyBid for historical unit prices
```

### Development Workflow

```bash
# 1. Create feature branch
/git-branch feature/add-auth

# 2. Implement changes
# ... make code changes ...

# 3. Review code
/review --focus security

# 4. Research best practices
@research-agent what are best practices for JWT token expiration?

# 5. Run tests and commit
# ... standard git workflow ...
```

### Data Processing Workflow

```bash
# 1. Extract data from Excel
/excel-automation read quarterly_sales.xlsx

# 2. Process and analyze
# Agent processes the data

# 3. Generate report
/excel-automation create summary report
```

## Community & Ecosystem

This toolkit follows patterns established by the growing agentic coding community:

**Similar Projects:**
- [PRPM.dev](https://prpm.dev/) - Large collection of Cursor rules and Claude agents (7,000+ packages)
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) - Curated list of Claude Code resources
- [VoltAgent Subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) - Specialized Claude Code subagents

**Ecosystem Standards:**
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP specification
- [Claude Code Docs](https://code.claude.com/docs) - Official documentation
- [MCP Servers](https://github.com/modelcontextprotocol/servers) - Reference implementations

## Roadmap

### Short Term
- [ ] Add more example commands
- [ ] Create agent library for common tasks
- [ ] Build adapter for more tools
- [ ] Comprehensive testing suite

### Medium Term
- [ ] NPM/pip package for easy installation
- [ ] Web-based configuration tool
- [ ] Community contribution guidelines
- [ ] Video tutorials and documentation

### Long Term
- [ ] Hosted MCP server marketplace
- [ ] AI-assisted component generation
- [ ] Cross-tool synchronization
- [ ] Enterprise features (team sharing, permissions)

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Add your component (command/agent/skill/server)
4. Test thoroughly
5. Document clearly
6. Submit a pull request

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines.

## Troubleshooting

### Commands not appearing
- Check installation path: `ls ~/.claude/commands/shared`
- Verify symlinks: `ls -la ~/.claude/commands/shared`
- Restart your AI host
- Check for syntax errors in command files

### Agents not working
- Verify agent file format (frontmatter + content)
- Check tool restrictions
- Review agent instructions for clarity
- Test with simple tasks first

### Skills not loading
- Ensure SKILL.md exists in skill directory
- Check script permissions: `chmod +x scripts/*.py`
- Verify Python dependencies are installed
- Review skill logs for errors

### MCP server not connecting
- Check server installation: `pip list | grep mcp`
- Verify configuration in mcp_settings.json
- Test server independently: `python -m server_name`
- Check server logs for connection errors

## Support

- **Documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/yourusername/shared-agent-toolkit/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/shared-agent-toolkit/discussions)
- **Community:** Join our Discord (link)

## License

MIT License - See [LICENSE](LICENSE) for details.

## Acknowledgments

This toolkit was inspired by:
- The Claude Code community and their innovative subagent patterns
- Anthropic's MCP standard and ecosystem
- The broader agentic coding community (Cursor, Aider, and others)
- Brandon Lewis's vision for shared construction industry tooling

Built with insights from:
- [Response Awareness Substack](https://responseawareness.substack.com/p/claude-code-subagents-the-orchestrators) - Orchestrator patterns
- [Product Talk](https://www.producttalk.org/how-to-use-claude-code-features/) - Claude Code features deep-dive
- [Sid Bharath's Guide](https://www.siddharthbharath.com/claude-code-the-complete-guide/) - Comprehensive Claude Code guide
- [MCP Documentation](https://modelcontextprotocol.io/) - Official MCP spec

---

**Built for the future of agentic coding. Version controlled. Portable. Shareable.**
