# Example MCP Server

This is a minimal example MCP (Model Context Protocol) server that demonstrates the basic structure and patterns for creating custom MCP servers.

## What is MCP?

MCP (Model Context Protocol) is an open standard for connecting AI assistants to data systems. It provides a standardized way for AI agents to access tools, resources, and prompts.

## Architecture

```
AI Host (Claude Code, Claude Desktop, Cursor, etc.)
    ↓
MCP Client
    ↓
MCP Server (this code)
    ↓
Your Data/Tools
```

## Server Capabilities

This example server provides:
- **Tools**: Functions the AI can invoke
- **Resources**: Data sources the AI can read
- **Prompts**: Reusable prompt templates

## Installation

```bash
cd mcp-servers/example-mcp
pip install -e .
```

## Configuration

Add to your MCP client configuration:

**Claude Code** (~/.claude/mcp_settings.json):
```json
{
  "mcpServers": {
    "example": {
      "command": "python",
      "args": ["-m", "example_mcp"],
      "env": {}
    }
  }
}
```

**Claude Desktop** (~/Library/Application Support/Claude/claude_desktop_config.json):
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

## Development

The server is implemented in `server.py` using the official MCP SDK:

```python
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("example")

@server.tool()
async def example_tool(param: str) -> str:
    """Example tool that processes input"""
    return f"Processed: {param}"
```

## Testing

```bash
# Install dependencies
pip install mcp

# Run server in stdio mode
python -m example_mcp

# Test with MCP inspector
mcp-inspector python -m example_mcp
```

## Creating Your Own MCP Server

1. Copy this directory as a template
2. Modify `server.py` to add your tools
3. Update `pyproject.toml` with your project info
4. Implement your business logic
5. Test with MCP inspector
6. Configure in your AI host

## Key Concepts

### Tools
Functions the AI can call with parameters:
```python
@server.tool()
async def calculate_sum(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
```

### Resources
Data sources the AI can read:
```python
@server.resource("config://settings")
async def get_settings() -> str:
    """Get application settings"""
    return json.dumps(settings)
```

### Prompts
Reusable prompt templates:
```python
@server.prompt()
async def code_review() -> str:
    """Prompt for code review"""
    return "Review this code for security and performance issues..."
```

## Best Practices

1. **Clear descriptions** - Tools and parameters should have helpful descriptions
2. **Type hints** - Use Python type hints for parameters
3. **Error handling** - Return meaningful error messages
4. **Validation** - Validate inputs before processing
5. **Documentation** - Document your tools and their behavior
6. **Security** - Be cautious with file system access and external commands
7. **Performance** - Long-running operations should provide progress updates

## Resources

- [MCP Specification](https://modelcontextprotocol.io/docs)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
