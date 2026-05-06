# 🌤️ WeatherWise AI

An intelligent weather assistant powered by AI agents with tool-calling capabilities. Get real-time weather forecasts using natural language queries!

## ✨ Features

- 🤖 **AI-Powered**: Uses advanced language models (Ollama, OpenRouter)
- 🛠️ **Tool Calling**: Automatically fetches real weather data from APIs
- 💬 **Natural Language**: Ask about weather in plain English
- 🔄 **Multiple Backends**: Supports both local (Ollama) and cloud (OpenRouter) models
- 🎯 **Interactive**: Chat-based interface for easy weather queries

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Ollama (for local models) OR OpenRouter API key (for cloud models)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/weatherwise-ai.git
cd weatherwise-ai
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install strands-agents strands-agents-tools python-dotenv litellm
```

### Setup

#### Option 1: Using Ollama (Local, Free)

1. Install Ollama from [ollama.ai](https://ollama.ai)

2. Pull a model with good tool support:
```bash
ollama pull llama3.1
```

3. Run the weather agent:
```bash
python main_ollama_fixed.py
```

#### Option 2: Using OpenRouter (Cloud)

1. Get an API key from [OpenRouter](https://openrouter.ai)

2. Create a `.env` file:
```bash
OPENROUTER_API_KEY=your-api-key-here
```

3. Run the weather agent:
```bash
python main.py
```

## 💡 Usage

```python
from strands import Agent
from strands.models.ollama import OllamaModel
from strands_tools import http_request

# Create weather agent
model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.1",
    temperature=0.3
)

agent = Agent(
    model=model,
    system_prompt="You are a helpful weather assistant...",
    tools=[http_request]
)

# Ask about weather
response = agent("What's the weather like in San Francisco?")
print(response)
```

## 📁 Project Structure

```
weatherwise-ai/
├── main.py                    # OpenRouter version
├── main_ollama_fixed.py       # Ollama version (recommended)
├── main_working.py            # Enhanced Ollama version
├── test_real_api.py          # API testing script
├── debug_tools.py            # Debugging utilities
├── .env                      # API keys (create this)
├── pyproject.toml            # Project metadata
└── README.md                 # This file
```

## 🔧 Configuration

### Ollama Models

Recommended models for best tool-calling support:
- `llama3.1` (8B) - Good balance
- `llama3.1:70b` - Best accuracy (requires more RAM)
- `qwen2.5-coder:7b` - Code-focused

### OpenRouter Models

Free and paid options:
- `google/gemini-flash-1.5` - Free
- `anthropic/claude-3.5-sonnet` - Paid, excellent tool support
- `meta-llama/llama-3.1-8b-instruct` - Free

## 🌐 API

Uses the [National Weather Service API](https://www.weather.gov/documentation/services-web-api) for weather data.

## ⚠️ Known Issues

- **Hallucination**: Smaller local models may sometimes generate fake weather data instead of using real API responses
- **Tool Execution**: Some models have better tool-calling capabilities than others
- **Rate Limits**: NWS API has rate limits for excessive requests

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📝 License

MIT License - feel free to use this project for learning and development!

## 🙏 Acknowledgments

- Built with [Strands](https://github.com/strands-ai/strands) - AI agent framework
- Weather data from [National Weather Service](https://www.weather.gov/)
- Powered by [Ollama](https://ollama.ai) and [OpenRouter](https://openrouter.ai)

## 📧 Contact

Questions? Open an issue or reach out!

---

Made with ❤️ using AI agents and tool calling
