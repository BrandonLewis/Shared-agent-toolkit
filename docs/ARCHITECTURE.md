# Architecture Overview

This document provides an in-depth look at the architectural patterns and design decisions behind the Shared Agent Toolkit.

## Design Philosophy

### 1. Portability First
Components should work across different AI coding assistants with minimal adaptation. This means:
- Standard formats (Markdown, YAML, Python)
- Minimal tool-specific dependencies
- Clear separation of concerns
- Adapter pattern for compatibility

### 2. Version Control Friendly
Everything should be text-based and git-friendly:
- No binary formats for configuration
- Clear diffs for changes
- Semantic versioning
- Tag-based releases

### 3. Composability
Components should work independently and together:
- Commands can invoke other commands
- Agents can delegate to sub-agents
- Skills can use multiple scripts
- MCP servers can integrate with other servers

### 4. Progressive Enhancement
Start simple, add complexity as needed:
- Basic commands with just markdown
- Add frontmatter for metadata
- Bundle scripts into skills
- Build MCP servers for complex integrations

## Component Architecture

### Commands

**Purpose:** Reusable prompt templates with optional parameters

**Why Markdown?**
- Human readable
- Easy to edit
- Version control friendly
- Supported by all markdown renderers
- Natural format for documentation

**Why YAML Frontmatter?**
- Standard pattern (Jekyll, Hugo, etc.)
- Easy to parse
- Structured metadata
- Optional (plain markdown works too)

**File Structure:**
```
commands/
└── category/
    └── command-name.md
```

**Namespacing:**
Directory structure creates natural namespaces:
- `/dev/review` → `commands/dev/review.md`
- `/construction/takeoff` → `commands/construction/takeoff.md`

**Evolution Path:**
1. Start: Simple markdown file
2. Add: YAML frontmatter for args
3. Enhance: Add examples and best practices
4. Scale: Create skill if scripts needed

### Agents (Subagents)

**Purpose:** Specialized AI assistants with focused context and tools

**Key Insight: Context Isolation**

Traditional approach:
```
Main Agent Context:
├── Orchestration logic
├── Implementation details ← Clutters context!
├── Debug information
└── Multiple concurrent tasks
```

Subagent approach:
```
Main Agent Context:
└── Orchestration logic only

Subagent 1 Context:
└── Implementation task A

Subagent 2 Context:
└── Implementation task B
```

**Benefits:**
- Main agent stays focused on orchestration
- Implementation details don't clutter main context
- Each subagent has clean, focused context
- Parallel execution possible
- Better token efficiency

**File Structure:**
```markdown
---
name: agent-name
description: Invocation criteria
tools: [Bash, Read, Write]
model: sonnet
---

You are a [role]...
```

**Tool Restrictions:**
- Limits what the agent can do
- Prevents unintended side effects
- Enforces single responsibility
- Improves security

**Model Selection:**
- `haiku` - Fast, cheap, simple tasks
- `sonnet` - Balanced, most use cases
- `opus` - Complex reasoning, expensive

### Skills

**Purpose:** Bundle prompts with executable code and resources

**Why Skills vs MCP?**

| Aspect | Skills | MCP |
|--------|--------|-----|
| Loading | On-demand | Upfront |
| Context | Only when used | Always loaded |
| Complexity | Simple | More complex |
| Portability | High | Medium |
| Power | Scripts + prompts | Full server |

**Use Skills When:**
- Task is domain-specific
- Need bundled scripts
- Want to include templates
- Don't need complex state

**Use MCP When:**
- Need persistent connection
- Complex external integrations
- Multiple tools in one package
- Cross-host compatibility critical

**Directory Structure:**
```
skills/skill-name/
├── SKILL.md              # Main instructions
├── README.md             # User documentation
├── scripts/              # Helper scripts
│   ├── script1.py
│   └── script2.sh
├── templates/            # File templates
│   └── template.txt
└── tests/               # Unit tests
    └── test_script1.py
```

**Lifecycle:**
1. AI reads SKILL.md instructions
2. AI determines which scripts to use
3. AI executes scripts with appropriate args
4. AI processes output and presents to user

### MCP Servers

**Purpose:** Standardized tool integration across AI hosts

**Architecture:**
```
┌─────────────────────────────────────┐
│         AI Host Layer               │
│  (Claude Code, Cursor, OpenAI SDK)  │
└──────────────┬──────────────────────┘
               │ MCP Client
               │
┌──────────────┴──────────────────────┐
│         MCP Server Layer            │
│  (Your custom integration)          │
├─────────────────────────────────────┤
│  ├── Tools (Functions)              │
│  ├── Resources (Data)               │
│  └── Prompts (Templates)            │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│      External Systems Layer         │
│  (Databases, APIs, File Systems)    │
└─────────────────────────────────────┘
```

**MCP Concepts:**

**Tools** - Functions the AI can invoke:
```python
@server.tool()
async def calculate_sum(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
```

**Resources** - Data the AI can read:
```python
@server.resource("data://users")
async def get_users() -> str:
    return json.dumps(users)
```

**Prompts** - Reusable templates:
```python
@server.prompt()
async def code_review() -> str:
    return "Review this code for..."
```

**Communication:**
- JSON-RPC over stdio
- Async operations supported
- Type-safe parameters
- Error handling built-in

**Security Considerations:**
- Validate all inputs
- Limit file system access
- Secure API credentials
- Rate limiting for external APIs
- Audit logging

## Cross-Tool Compatibility

### Adaptation Strategy

```
┌─────────────────────┐
│  Shared Toolkit     │
│  (Universal format) │
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     │  Adapter  │
     └─────┬─────┘
           │
    ┌──────┴──────────┐
    │                 │
┌───▼───┐      ┌─────▼─────┐
│Claude │      │  Cursor   │
│ Code  │      │  (rules)  │
└───────┘      └───────────┘
```

### Format Translations

**Claude Code → Cursor:**
```python
# Input: commands/review.md
---
description: Code review
args: [...]
---
Instructions...

# Output: .cursor/rules/review.md
# review
Code review
Instructions...
```

**Universal → Aider:**
```python
# Aider uses simpler format
# Adapter strips frontmatter
# Keeps just instructions
```

## Installation Architecture

### Symlink Strategy

**Advantages:**
- Single source of truth
- Updates propagate automatically
- No duplication
- Easy to manage

**Structure:**
```
~/code/shared-agent-toolkit/     ← Repository
        │
        └── commands/
             └── dev/review.md

~/.claude/                        ← Claude Code config
    └── commands/
        └── shared/               ← Symlink
             └── dev/review.md    ← Accessible via symlink
```

**Implementation:**
```bash
ln -sf ~/code/shared-agent-toolkit/commands ~/.claude/commands/shared
```

**Result:**
Command accessible as: `/shared/dev/review`

### Alternative: Copy Strategy

For environments where symlinks don't work:
```bash
# Copy instead of symlink
cp -r commands ~/.claude/commands/shared

# Need update mechanism
./install.sh --update
```

## Data Flow

### Command Invocation
```
User: /review --focus security
  ↓
AI Host loads command from file
  ↓
Parses frontmatter for args
  ↓
Replaces {{placeholders}}
  ↓
Executes with filled template
  ↓
Returns result to user
```

### Agent Delegation
```
User: @research-agent find rate limiting patterns
  ↓
Main Agent (orchestrator)
  ↓
Loads research-agent.md
  ↓
Creates isolated context
  ↓
Sub-agent executes with tools
  ↓
Returns result to main agent
  ↓
Main agent synthesizes and responds
```

### Skill Execution
```
User: /excel-automation extract data
  ↓
AI loads SKILL.md
  ↓
Determines required script
  ↓
Executes: scripts/excel_reader.py
  ↓
Processes script output
  ↓
Presents formatted result
```

### MCP Tool Call
```
User: "Calculate takeoff for asphalt"
  ↓
AI decides to use construction MCP
  ↓
Calls tool: calculate_takeoff(...)
  ↓
MCP Server processes request
  ↓
Accesses HeavyBid database
  ↓
Returns structured result
  ↓
AI formats for user
```

## Scaling Considerations

### Performance

**Commands:**
- Instant load (small text files)
- No runtime overhead
- Cache-friendly

**Agents:**
- New context per invocation
- Token cost per agent
- Parallel execution possible

**Skills:**
- On-demand script execution
- External process overhead
- Can be async

**MCP Servers:**
- Persistent connection
- Initialization cost
- Amortized over multiple calls

### Organization

**Small Project (< 20 components):**
```
commands/
  ├── common/
  └── project-specific/
agents/
  └── 2-3 specialized agents
```

**Medium Project (20-100 components):**
```
commands/
  ├── common/
  ├── domain-a/
  └── domain-b/
agents/
  ├── domain-specific/
  └── utility/
skills/
  └── 3-5 skills
```

**Large Project (100+ components):**
```
commands/
  ├── common/
  ├── domains/
  │   ├── domain-a/
  │   ├── domain-b/
  │   └── domain-c/
  └── internal/
agents/
  ├── specialized/
  ├── utility/
  └── orchestrators/
skills/
  └── 10+ skills organized by domain
mcp-servers/
  └── Multiple servers by integration
```

## Future Directions

### Potential Enhancements

1. **Dynamic Loading**
   - Hot reload on file change
   - No restart required

2. **Composition**
   - Commands that invoke other commands
   - Agent hierarchies
   - Skill dependencies

3. **Validation**
   - Schema validation for frontmatter
   - Lint commands for best practices
   - Test agent behavior

4. **Discovery**
   - Auto-generate command index
   - Search across all components
   - Suggest relevant commands

5. **Marketplace**
   - Share components publicly
   - Version compatibility
   - Dependency management

---

This architecture balances simplicity with power, portability with capability, and immediate usability with future extensibility.
