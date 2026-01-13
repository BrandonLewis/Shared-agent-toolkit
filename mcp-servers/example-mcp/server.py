#!/usr/bin/env python3
"""
Example MCP Server
Demonstrates basic MCP server implementation with tools, resources, and prompts
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List

try:
    from mcp.server import Server
    from mcp.types import Tool, Resource, Prompt, TextContent
except ImportError:
    print("Error: mcp package not installed. Install with: pip install mcp")
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("example-mcp")

# Initialize server
server = Server("example-mcp")

# Sample data store (in real application, this would be a database or API)
data_store = {
    "users": [
        {"id": 1, "name": "Alice", "role": "Engineer"},
        {"id": 2, "name": "Bob", "role": "Manager"},
    ],
    "config": {
        "version": "1.0.0",
        "environment": "development"
    }
}


# ============================================================================
# TOOLS - Functions the AI can call
# ============================================================================

@server.tool()
async def get_current_time() -> str:
    """Get the current date and time"""
    return datetime.now().isoformat()


@server.tool()
async def calculate_sum(a: float, b: float) -> float:
    """
    Add two numbers together

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    result = a + b
    logger.info(f"Calculated sum: {a} + {b} = {result}")
    return result


@server.tool()
async def search_users(query: str) -> List[Dict[str, Any]]:
    """
    Search for users by name

    Args:
        query: Search query string

    Returns:
        List of matching users
    """
    query_lower = query.lower()
    results = [
        user for user in data_store["users"]
        if query_lower in user["name"].lower()
    ]
    logger.info(f"Search for '{query}' returned {len(results)} results")
    return results


@server.tool()
async def create_user(name: str, role: str) -> Dict[str, Any]:
    """
    Create a new user

    Args:
        name: User's name
        role: User's role

    Returns:
        Created user object
    """
    new_id = max(u["id"] for u in data_store["users"]) + 1
    new_user = {"id": new_id, "name": name, "role": role}
    data_store["users"].append(new_user)
    logger.info(f"Created user: {new_user}")
    return new_user


@server.tool()
async def format_json(data: str, indent: int = 2) -> str:
    """
    Format JSON string with proper indentation

    Args:
        data: JSON string to format
        indent: Number of spaces for indentation

    Returns:
        Formatted JSON string
    """
    try:
        parsed = json.loads(data)
        formatted = json.dumps(parsed, indent=indent)
        return formatted
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON - {str(e)}"


# ============================================================================
# RESOURCES - Data sources the AI can read
# ============================================================================

@server.resource("data://users")
async def get_users_resource() -> str:
    """Get all users from the data store"""
    return json.dumps(data_store["users"], indent=2)


@server.resource("data://config")
async def get_config_resource() -> str:
    """Get application configuration"""
    return json.dumps(data_store["config"], indent=2)


@server.resource("data://stats")
async def get_stats_resource() -> str:
    """Get system statistics"""
    stats = {
        "timestamp": datetime.now().isoformat(),
        "total_users": len(data_store["users"]),
        "server_version": "1.0.0"
    }
    return json.dumps(stats, indent=2)


# ============================================================================
# PROMPTS - Reusable prompt templates
# ============================================================================

@server.prompt()
async def analyze_data() -> str:
    """Prompt template for data analysis"""
    return """You are a data analyst. Analyze the provided data and:

1. Identify key patterns and trends
2. Calculate relevant statistics
3. Highlight any anomalies
4. Provide actionable insights

Present your findings in a clear, structured format."""


@server.prompt()
async def code_review() -> str:
    """Prompt template for code review"""
    return """You are a senior software engineer performing a code review. Evaluate the code for:

**Security:**
- Input validation
- Authentication/authorization
- Data exposure risks
- Known vulnerabilities

**Quality:**
- Readability and maintainability
- Proper error handling
- Code organization
- Test coverage

**Performance:**
- Algorithm efficiency
- Resource usage
- Potential bottlenecks

Provide specific, actionable feedback with severity ratings (Critical/Major/Minor)."""


@server.prompt()
async def user_onboarding(username: str) -> str:
    """
    Prompt template for user onboarding

    Args:
        username: Name of the user being onboarded
    """
    return f"""You are helping onboard a new user: {username}

Guide them through:
1. System overview and key features
2. Account setup and configuration
3. Best practices and tips
4. Common workflows
5. Where to get help

Be friendly, clear, and concise. Use examples where helpful."""


# ============================================================================
# SERVER LIFECYCLE
# ============================================================================

@server.on_initialize()
async def on_initialize():
    """Called when the server initializes"""
    logger.info("Example MCP server initialized")


@server.on_shutdown()
async def on_shutdown():
    """Called when the server shuts down"""
    logger.info("Example MCP server shutting down")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Run the MCP server"""
    import asyncio
    from mcp.server.stdio import stdio_server

    logger.info("Starting Example MCP Server...")

    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )

    asyncio.run(run())


if __name__ == "__main__":
    main()
