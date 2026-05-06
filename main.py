import os
from strands import Agent
from strands.models.litellm import LiteLLMModel  # Use LiteLLM for OpenRouter
from strands_tools import http_request
from dotenv import load_dotenv
load_dotenv()

# Get OpenRouter API key from environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# Define a detailed system prompt to guide the agent's behavior
WEATHER_SYSTEM_PROMPT = """You are a friendly and helpful weather assistant with HTTP capabilities.

Your primary function is to provide accurate weather forecasts for locations in the United States by using the National Weather Service API.

IMPORTANT: Follow these steps EXACTLY to fulfill a user's request:

Step 1: Get the forecast URL
- For latitude and longitude: Call https://api.weather.gov/points/{latitude},{longitude}
- For a US zipcode: Call https://api.weather.gov/points/{zipcode}
- Extract the "forecast" URL from the response's "properties" field

Step 2: Get the actual weather forecast
- Use the forecast URL from Step 1 to make a second HTTP request
- This will return the actual weather data with temperatures and conditions

Step 3: Present the results
- Show temperature, conditions, and forecast details
- Explain in simple, friendly language
- If you encounter an error, apologize and explain what went wrong

CRITICAL: You MUST make TWO API calls - first to get the forecast URL, then to that URL to get the weather data.
"""

# Configure OpenRouter with a working free model
openrouter_model = LiteLLMModel(
    model_id="openrouter/google/gemini-flash-1.5",  # Free Google model with tool support
    params={
        "api_key": OPENROUTER_API_KEY,
        "temperature": 0.7,
        "max_tokens": 4096
    }
)

# Create agent with OpenRouter model
weather_agent = Agent(
    model=openrouter_model,
    system_prompt=WEATHER_SYSTEM_PROMPT,
    tools=[http_request]
)

# Example usage - Interactive mode
if __name__ == "__main__":
    print("Weather Assistant (powered by Ollama)")
    print("=" * 50)
    
    while True:
        user_input = input("\nAsk about weather (or 'quit' to exit): ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
            
        response = weather_agent(user_input)
        print("\n" + "=" * 50)
        print(response)
        print("=" * 50)
 