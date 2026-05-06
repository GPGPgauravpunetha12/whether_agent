"""
Lesson 2: Session Management (Memory)

This script demonstrates how to give your agent memory by using a session manager.

A session manager automatically saves and loads an agent's conversation history,
allowing it to remember past interactions and maintain context. We'll use the
`FileSessionManager` which persists the session to the local filesystem.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from strands import Agent

from strands.models.ollama import OllamaModel
from strands.session.file_session_manager import FileSessionManager

# Load environment variables from a .env file
load_dotenv()


def create_persistent_agent(session_id: str) -> Agent:
    """
    Creates an agent with persistent memory using a FileSessionManager.

    Args:
        session_id: A unique identifier for the conversation session.

    Returns:
        An Agent instance that can remember past interactions.
    """
    # Configure the language model
    ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.1",  # Better tool support than qwen2.5-coder
    temperature=0.3,  # Lower for more focused responses
    max_tokens=4096,
    keep_alive="10m"
    )
    # Set up the directory to store session files
    base_dir = Path(__file__).parent.resolve()
    storage_dir = base_dir / "tmp" / "sessions"
    print(f"Session files will be stored in: {storage_dir}")

    # Create a FileSessionManager to handle saving and loading the conversation
    session_manager = FileSessionManager(
        session_id=session_id,
        storage_dir=str(storage_dir),
    )

    # Create an agent and attach the session manager
    # This agent will now have memory!
    persistent_agent = Agent(
        model=ollama_model,  # Fixed: use ollama_model instead of model
        session_manager=session_manager,
        system_prompt="You are a friendly assistant. Keep your responses concise."
    )
    return persistent_agent


def main():
    """
    Main function to demonstrate a conversational agent with memory.
    """
    # Each session ID represents a unique conversation history
    session_id = "user_gaurav_convo_123"
    agent = create_persistent_agent(session_id)

    print("--- Conversation Start ---")

    # First interaction: The user introduces themselves
    print("\nUser: Hey, my name is gaurav .")
    response1 = agent("Hey, my name is gaurav/")
    print(f"Agent: {response1}")

    # Second interaction: Ask the agent if it remembers the name
    print("\nUser: Do you remember my name?")
    response2 = agent("Do you remember my name?")
    print(f"Agent: {response2}")

    print("\n--- Conversation End ---")
    print(f"\nThe agent was able to remember the name because its memory is persisted in the session '{session_id}'.")


if __name__ == "__main__":
    main()