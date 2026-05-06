import os
from strands import Agent
from strands.models.ollama import OllamaModel
from strands_tools import http_request
from dotenv import load_dotenv
load_dotenv()

# System prompt optimized for Ollama
WEATHER_SYSTEM_PROMPT = """You are a weather assistant with access to the http_request tool.

When asked about weather, you MUST:
1. Call http_request to get forecast URL from https://api.weather.gov/points/{lat},{lon}
2. Extract the "forecast" URL from the response
3. Call http_request again with that forecast URL
4. Report the weather from the second response

Always use the tool to get real data."""

# Configure Ollama - using llama3.1 which has better tool support
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.1",  # Better tool support than qwen2.5-coder
    temperature=0.3,  # Lower for more focused responses
    max_tokens=4096,
    keep_alive="10m"
)

# Create agent
weather_agent = Agent(
    model=ollama_model,
    system_prompt=WEATHER_SYSTEM_PROMPT,
    tools=[http_request]
)

# Interactive mode
if __name__ == "__main__":
    print("Weather Assistant (powered by Ollama - Llama 3.1)")
    print("=" * 50)
    print("Note: Make sure you have llama3.1 installed:")
    print("  ollama pull llama3.1")
    print("=" * 50)
    
    while True:
        user_input = input("\nAsk about weather (or 'quit' to exit): ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
            
        try:
            response = weather_agent(user_input)
            print("\n" + "=" * 50)
            print(response)
            print("=" * 50)
        except Exception as e:
            print(f"\nError: {e}")
            print("Make sure Ollama is running and llama3.1 is installed")
