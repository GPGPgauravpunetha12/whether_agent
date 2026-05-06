"""
Lesson 4: MCP (Model Context Protocol) - Simplified Demo

This demonstrates the concept of MCP without requiring external servers.
MCP allows agents to dynamically load tools from external sources.

For a full MCP demo with AWS documentation, see mcp_demo.py
(Note: That requires uvx and may take time to download MCP servers)
"""

import os
from dotenv import load_dotenv
from strands import Agent
from strands.models.ollama import OllamaModel
from strands_tools import http_request, calculator

load_dotenv()

print("=" * 70)
print("MCP Concept Demo: Dynamic Tool Loading")
print("=" * 70)

# Configure model
model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.1",
    temperature=0.3,
    max_tokens=2048
)

# Simulate MCP-like behavior: dynamically load tools
print("\n📦 Loading tools dynamically (MCP-style)...")
available_tools = [http_request, calculator]
print(f"✅ Loaded {len(available_tools)} tools:")
for tool in available_tools:
    print(f"   - {tool.__name__}")

# Create agent with dynamically loaded tools
agent = Agent(
    model=model,
    tools=available_tools,
    system_prompt=(
        "You are a helpful assistant with access to external tools. "
        "Use the calculator for math and http_request for web data."
    )
)

print("\n" + "=" * 70)
print("Testing Agent with Dynamically Loaded Tools")
print("=" * 70)

# Test 1: Calculator tool
print("\n🧮 Test 1: Using calculator tool")
print("Query: What is 25 * 48 + 100?")
response1 = agent("What is 25 * 48 + 100?")
print(f"Response: {response1}")

print("\n" + "=" * 70)
print("\n💡 MCP Concept Explained:")
print("""
MCP (Model Context Protocol) allows:
1. ✅ Dynamic tool loading from external servers
2. ✅ Agents can gain new capabilities at runtime
3. ✅ Tools can be shared across different agents
4. ✅ Standardized protocol for tool communication

Real MCP servers (like AWS docs) provide:
- Documentation search
- API integrations
- Database queries
- And much more!

To try the full AWS documentation MCP demo:
  python mcp_demo.py
  (Note: May take time to download MCP server)
""")
print("=" * 70)
