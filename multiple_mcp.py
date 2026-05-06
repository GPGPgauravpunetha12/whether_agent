"""
Multiple MCP Servers Integration Example

This script demonstrates how to connect an agent to multiple MCP servers
simultaneously, combining their tools to create a more powerful agent.

In this example, we connect to:
1. AWS Documentation MCP server - for AWS documentation search
2. SearchAPI MCP server - for Airbnb search capabilities

The agent can then use tools from both servers to answer complex queries.
"""

from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.models.ollama import OllamaModel
from strands.tools.mcp import MCPClient
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("🌐 Multiple MCP Servers Demo")
print("=" * 70)

# Configure Ollama model
model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.1",
    temperature=0.3,
    max_tokens=4096,
    keep_alive="10m"
)

print("\n📦 Setting up MCP clients...")
print("This may take a moment to download servers if needed...\n")

# Set up AWS Documentation MCP client
print("1. Connecting to AWS Documentation MCP server...")
aws_mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx", 
            args=["awslabs.aws-documentation-mcp-server@latest"]
        )
    )
)

# Set up SearchAPI MCP client for Airbnb
print("2. Connecting to SearchAPI MCP server (Airbnb)...")
searchapi_mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="npx",
            args=["-y", "mcp-remote", "https://www.searchapi.io/mcp?token=TzYTv6sn9CKsKfrpudargZp4"]
        )
    )
)

# Use both servers together and create agent
try:
    with aws_mcp_client, searchapi_mcp_client:
        # Combine tools from both servers
        aws_tools = aws_mcp_client.list_tools_sync()
        searchapi_tools = searchapi_mcp_client.list_tools_sync()
        all_tools = aws_tools + searchapi_tools

        print(f"\n✅ Loaded {len(aws_tools)} AWS documentation tools")
        print(f"✅ Loaded {len(searchapi_tools)} SearchAPI tools")
        print(f"✅ Total tools available: {len(all_tools)}")

        # Create agent with all tools from both servers
        agent = Agent(
            tools=all_tools,
            model=model,
            system_prompt=(
                "You are a helpful assistant with access to AWS documentation "
                "and Airbnb search capabilities. Use the appropriate tools "
                "to help users find information."
            ),
        )

        print("\n" + "=" * 70)
        print("🔍 Query 1: AWS Documentation")
        print("=" * 70)
        
        # Query 1: AWS documentation
        user_query = "What is AWS Lambda's maximum execution time?"
        print(f"\nUser Query: {user_query}\n")

        response = agent(user_query)

        print("\n--- Agent Response ---")
        print(response)

        print("\n" + "=" * 70)
        print("🏠 Query 2: Airbnb Search")
        print("=" * 70)
        
        # Query 2: Airbnb search
        user_query_2 = "Find Airbnb properties in Barcelona for 2 adults"
        print(f"\nUser Query: {user_query_2}\n")

        response = agent(user_query_2)

        print("\n--- Agent Response ---")
        print(response)
        
        print("\n" + "=" * 70)
        print("✅ Multi-MCP Demo Complete!")
        print("=" * 70)
        
        print("""
💡 What Just Happened:

1. ✅ Connected to 2 MCP servers:
   - AWS Documentation (technical docs)
   - SearchAPI (Airbnb search)

2. ✅ Combined tools from both servers

3. ✅ Single agent can use tools from multiple sources

4. ✅ Demonstrates multi-server MCP architecture

This shows how MCP enables agents to access
multiple specialized tool servers simultaneously!
""")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nNote: This requires 'uvx' and 'npx' to be installed.")
    print("Install Node.js from: https://nodejs.org/")
    print("Install uv from: https://docs.astral.sh/uv/")