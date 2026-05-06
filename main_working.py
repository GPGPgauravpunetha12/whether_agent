import os
from strands import Agent
from strands.models.ollama import OllamaModel
from strands_tools import http_request
from dotenv import load_dotenv
load_dotenv()

# More explicit system prompt
WEATHER_SYSTEM_PROMPT = """You are a weather assistant. You have access to http_request tool.

CRITICAL RULES:
1. You MUST use the http_request tool to get real data
2. NEVER make up weather data
3. Always show the actual JSON response from the API
4. If the tool fails, say "I couldn't fetch the weather data"

Steps:
1. Call: https://api.weather.gov/points/{latitude},{longitude}
2. Look for "forecast" URL in the response
3. Call that forecast URL
4. Report what you actually received"""

# Using llama3.1 with stricter settings
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.1",
    temperature=0.1,  # Very low to reduce hallucination
    max_tokens=2048,
    keep_alive="10m"
)

weather_agent = Agent(
    model=ollama_model,
    system_prompt=WEATHER_SYSTEM_PROMPT,
    tools=[http_request]
)

if __name__ == "__main__":
    print("🌤️  Weather Assistant (Ollama + Llama 3.1)")
    print("=" * 60)
    
    # Test with a specific location
    print("\nTesting with San Francisco (37.7749, -122.4194)...")
    print("=" * 60)
    
    response = weather_agent(
        "Get the weather for San Francisco at coordinates 37.7749, -122.4194. "
        "Show me the actual API response data."
    )
    
    print("\n" + response)
    print("=" * 60)
    
    # Interactive mode
    print("\n\nInteractive Mode:")
    while True:
        user_input = input("\nAsk about weather (or 'quit'): ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
            
        try:
            response = weather_agent(user_input)
            print("\n" + "=" * 60)
            print(response)
            print("=" * 60)
        except Exception as e:
            print(f"\n❌ Error: {e}")
