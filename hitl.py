"""
Lesson 5: Human-in-the-Loop (HITL)

This script demonstrates how to incorporate human feedback into an agent's
workflow using the `handoff_to_user` tool.

This pattern is essential for:
- Tasks that require human approval before proceeding
- Situations where the agent needs clarifying questions
- Workflows where control needs to be returned to the user
"""

from strands import Agent
from strands.models.ollama import OllamaModel
from strands_tools import handoff_to_user

print("=" * 70)
print("🤝 Human-in-the-Loop (HITL) Demo")
print("=" * 70)


def create_interactive_agent() -> Agent:
    """
    Creates an agent equipped with the handoff_to_user tool.

    Returns:
        An Agent instance capable of interacting with a human user.
    """
    # Configure Ollama model
    model = OllamaModel(
        host="http://localhost:11434",
        model_id="llama3.1",
        temperature=0.3,
        max_tokens=2048,
        keep_alive="10m"
    )

    # Create the agent with handoff_to_user tool
    interactive_agent = Agent(
        tools=[handoff_to_user],
        model=model,
        system_prompt="You are a helpful assistant that can ask for user approval before taking actions.",
    )
    return interactive_agent


def format_handoff_summary(response: dict | None, title: str) -> str:
    """Formats the response from a handoff_to_user call for display."""
    if not response:
        return f"--- {title}: No response ---"
  
    # Extract the agent's message to the user
    agent_message = "No message from agent."
    if "content" in response and response["content"]:
        agent_message = response["content"][0].get("text", agent_message).strip()

    summary_lines = [
        f"--- {title} ---",
        f'Agent Message: "{agent_message}"',
        f"Status       : {response.get('status', 'unknown').upper()}",
        f"Reference ID : {response.get('toolUseId', 'N/A')}",
    ]
    return "\n".join(summary_lines)


def main():
    """
    Main function to demonstrate the human-in-the-loop pattern.
    """
    agent = create_interactive_agent()

    print("\n--- Demonstrating Human-in-the-Loop ---\n")

    # Case 1: Requesting approval to continue
    print("📋 Use Case 1: Agent asks for approval and continues")
    print("-" * 70)
    approval_response = agent.tool.handoff_to_user(
        message="I have a plan to format the hard drive. Is it okay to proceed? Please type 'yes' to approve or 'no' to cancel.",
        breakout_of_loop=False,  # Agent continues after user responds
    )
    print(approval_response)
    print(format_handoff_summary(approval_response, "Approval Handoff"))

    # Case 2: Completing a task and stopping
    print("\n📋 Use Case 2: Agent completes its task and stops")
    print("-" * 70)
    completion_response = agent.tool.handoff_to_user(
        message="The task has been completed successfully. I will now stop.",
        breakout_of_loop=True,  # Agent stops execution
    )
    print(format_handoff_summary(completion_response, "Completion Handoff"))

    print("\n" + "=" * 70)
    print("✅ HITL Demo Complete!")
    print("=" * 70)
    
    print("""
💡 Key Concepts:

1. breakout_of_loop=False
   - Agent asks for approval
   - Continues after user responds
   - Used for confirmations

2. breakout_of_loop=True
   - Agent completes task
   - Stops execution
   - Returns control to user

This pattern is crucial for:
✅ Safety-critical operations
✅ User confirmations
✅ Interactive workflows
✅ Compliance requirements
""")


if __name__ == "__main__":
    main()