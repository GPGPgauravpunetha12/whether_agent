"""
Multi-Agent Travel Assistant System

This demonstrates a multi-agent system where different agents specialize in:
1. Web Search Agent - Uses Exa AI for current information
2. Accommodation Agent - Uses SearchAPI for Airbnb search
3. Coordinator Agent - Orchestrates both capabilities

Each agent has specific tools and expertise.
"""

import requests
from strands import Agent
from strands.models.ollama import OllamaModel
from strands.tools import tool

# API Keys
EXA_API_KEY = "0fe705af-b02a-498a-9ca0-edc6fe868920"
SEARCHAPI_KEY = "ERuxchM8EtLss5FtvLeEsgb1"

print("=" * 70)
print("🤖 Multi-Agent Travel Assistant System")
print("=" * 70)

# Configure Ollama model (shared by all agents)
def create_model():
    return OllamaModel(
        host="http://localhost:11434",
        model_id="llama3.1",
        temperature=0.3,
        max_tokens=2048,
        keep_alive="10m"
    )

# ============================================================================
# TOOL DEFINITIONS
# ============================================================================

@tool
def search_web(query: str) -> str:
    """
    Search the web using Exa AI for current information.
    
    Args:
        query: The search query
        
    Returns:
        Search results as a string
    """
    try:
        url = "https://api.exa.ai/search"
        headers = {
            "x-api-key": EXA_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "query": query,
            "num_results": 3,
            "type": "auto"
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            results = response.json()
            if "results" in results:
                output = []
                for i, result in enumerate(results["results"][:3], 1):
                    title = result.get("title", "No title")
                    url = result.get("url", "")
                    snippet = result.get("text", "")[:200]
                    output.append(f"{i}. {title}\n   URL: {url}\n   {snippet}...")
                return "\n\n".join(output)
        
        return f"Search failed with status {response.status_code}"
    except Exception as e:
        return f"Search error: {str(e)}"


@tool
def search_airbnb(location: str, checkin: str = "", checkout: str = "", adults: int = 2) -> str:
    """
    Search for Airbnb accommodations in a specific location.
    
    Args:
        location: City or location to search (e.g., "Barcelona", "Paris")
        checkin: Check-in date (optional, format: YYYY-MM-DD)
        checkout: Check-out date (optional, format: YYYY-MM-DD)
        adults: Number of adults (default: 2)
        
    Returns:
        Airbnb search results as a string
    """
    try:
        url = "https://www.searchapi.io/api/v1/search"
        params = {
            "engine": "airbnb",
            "q": location,
            "adults": adults,
            "api_key": SEARCHAPI_KEY
        }
        
        if checkin:
            params["check_in_date"] = checkin
        if checkout:
            params["check_out_date"] = checkout
        
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if "properties" in data and len(data["properties"]) > 0:
                properties = data["properties"][:3]
                output = []
                
                for i, prop in enumerate(properties, 1):
                    title = prop.get("title", "No title")
                    rating = prop.get("rating", "N/A")
                    reviews = prop.get("reviews", 0)
                    link = prop.get("link", "")
                    
                    price_info = prop.get("price", {})
                    total_price = price_info.get("total_price", "N/A")
                    
                    accommodations = prop.get("accommodations", [])
                    accommodations_str = ", ".join(accommodations) if accommodations else "N/A"
                    
                    output.append(
                        f"{i}. {title}\n"
                        f"   Rating: {rating} ({reviews} reviews)\n"
                        f"   Accommodations: {accommodations_str}\n"
                        f"   Total Price: {total_price}\n"
                        f"   Link: {link}"
                    )
                
                return "\n\n".join(output)
            else:
                return f"No properties found for {location}."
        
        return f"Airbnb search failed with status {response.status_code}"
    except Exception as e:
        return f"Airbnb search error: {str(e)}"


# ============================================================================
# SPECIALIZED AGENTS
# ============================================================================

print("\n🔧 Creating specialized agents...\n")

# Agent 1: Web Search Specialist
web_search_agent = Agent(
    model=create_model(),
    tools=[search_web],
    system_prompt=(
        "You are a web search specialist. Use the search_web tool to find "
        "current information about travel and destinations."
    )
)
print("✅ Web Search Agent created")

# Agent 2: Accommodation Specialist
accommodation_agent = Agent(
    model=create_model(),
    tools=[search_airbnb],
    system_prompt=(
        "You are an accommodation specialist. Use the search_airbnb tool "
        "to find Airbnb listings based on location and dates."
    )
)
print("✅ Accommodation Agent created")

# Agent 3: Coordinator Agent
coordinator_agent = Agent(
    model=create_model(),
    system_prompt=(
        "You are a travel coordinator. Help users plan trips by providing "
        "information about transportation and accommodations."
    ),
    tools=[search_web, search_airbnb]
)
print("✅ Coordinator Agent created")

# ============================================================================
# DEMO QUERIES
# ============================================================================

print("\n" + "=" * 70)
print("🔍 Demo 1: Web Search Agent")
print("=" * 70)

query1 = "What's the fastest way to travel from London to Barcelona?"
print(f"\nQuery: {query1}\n")
response1 = web_search_agent(query1)
print(f"Response:\n{response1}")

print("\n" + "=" * 70)
print("🏠 Demo 2: Accommodation Agent")
print("=" * 70)

query2 = "Find Airbnb accommodations in Barcelona for 2 adults"
print(f"\nQuery: {query2}\n")
response2 = accommodation_agent(query2)
print(f"Response:\n{response2}")

print("\n" + "=" * 70)
print("🎯 Demo 3: Coordinator Agent (Uses Both Tools)")
print("=" * 70)

query3 = "I want to visit Barcelona. Help me find travel options and places to stay."
print(f"\nQuery: {query3}\n")
response3 = coordinator_agent(query3)
print(f"Response:\n{response3}")

print("\n" + "=" * 70)
print("✅ Multi-Agent Demo Complete!")
print("=" * 70)

print("""
💡 Summary:

✅ 3 specialized agents created
✅ Each agent has specific tools and expertise
✅ Agents can work independently or together
✅ Real API calls to Exa AI and SearchAPI

This demonstrates a multi-agent system where different
agents specialize in different tasks!
""")
