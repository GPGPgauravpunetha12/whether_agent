"""
Lesson 4: Understanding MCP (Model Context Protocol)

This script explains what MCP is and how it works, without requiring
long-running agent calls or external servers.
"""

print("=" * 70)
print("🔌 MCP (Model Context Protocol) - Explained")
print("=" * 70)

print("""
## What is MCP?

MCP is a standardized protocol that allows AI agents to:
✅ Connect to external tool servers
✅ Dynamically load new capabilities
✅ Access real-time data and services
✅ Share tools across different agents

## How It Works:

1. **MCP Server** - Provides tools (e.g., AWS docs, databases, APIs)
2. **MCP Client** - Connects agent to the server
3. **Agent** - Uses tools to answer questions

## Example Flow:

User: "What is AWS Lambda's payload limit?"
  ↓
Agent connects to AWS Documentation MCP Server
  ↓
Agent uses 'search_aws_docs' tool
  ↓
Agent gets real documentation
  ↓
Agent responds with accurate info

## Available MCP Servers:

- **AWS Documentation** - Search AWS docs
- **GitHub** - Repository operations
- **Filesystem** - File operations
- **Database** - SQL queries
- **Web Search** - Internet search
- **Custom Servers** - Build your own!

## Code Example:

```python
from mcp import StdioServerParameters, stdio_client
from strands.tools.mcp import MCPClient

# Connect to AWS docs MCP server
mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx",
            args=["awslabs.aws-documentation-mcp-server@latest"]
        )
    )
)

# Load tools from the server
with mcp_client:
    tools = mcp_client.list_tools_sync()
    
    # Create agent with MCP tools
    agent = Agent(
        model=model,
        tools=tools  # Tools from MCP server!
    )
```

## Benefits:

1. **Dynamic** - Add tools without changing code
2. **Reusable** - Share tools across projects
3. **Standardized** - Common protocol for all tools
4. **Scalable** - Connect to multiple servers
5. **Up-to-date** - Tools always have latest data

## Try It Yourself:

Run the full MCP demo (requires uvx):
  python mcp_demo.py

Or check out MCP servers at:
  https://github.com/modelcontextprotocol

""")

print("=" * 70)
print("✅ MCP Concept Explained!")
print("=" * 70)
