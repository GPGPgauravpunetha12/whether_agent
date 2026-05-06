"""
Lesson 4: Integrating External Tools with MCP

This script demonstrates how to dynamically grant an agent new capabilities
by connecting it to an external tool server using the Multi-Capability
Protocol (MCP).

We will connect to a public MCP server that provides tools for searching
the official AWS documentation, allowing our agent to answer questions
about AWS services with up-to-date information.
"""

import os
from dotenv import load_dotenv
from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.models.ollama import OllamaModel
from strands.tools.mcp import MCPClient

load_dotenv()

# Configure the Ollama model
model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.1",
    temperature=0.3,
    max_tokens=4096,
    keep_alive="10m"
)

print("Setting up MCP client to connect to AWS documentation server...")
print("This may take a moment as it downloads the server if needed...\n")

# Set up MCP client to connect to AWS documentation server
mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx", args=["awslabs.aws-documentation-mcp-server@latest"]
        )
    )
)

# Create agent with AWS documentation tools
try:
    with mcp_client:
        aws_tools = mcp_client.list_tools_sync()
        print(f"✅ Successfully loaded {len(aws_tools)} tools from the MCP server.\n")
        
        print(f"Available AWS Documentation Tools: {len(aws_tools)} tools loaded\n")

        agent = Agent(
            model=model,
            tools=aws_tools,
            system_prompt=(
                "You are an expert on Amazon Web Services. "
                "Use the provided tools to answer questions about AWS services "
                "based on the official documentation. Always provide accurate, "
                "up-to-date information from the AWS docs."
            ),
        )

        # Query the agent
        user_query = "What is the maximum invocation payload size for AWS Lambda?"
        print("--- Querying AWS Documentation ---")
        print(f"User Query: {user_query}\n")

        response = agent(user_query)

        print("--- Agent Response ---")
        print(response)
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nNote: This script requires 'uvx' to be installed.")
    print("Install it with: pip install uv")
    print("Or on Windows: pip install uv")