# Barbie Movie Expert Chatbot

A sophisticated AI-powered chatbot application that provides information about Barbie movies using Google's Gemini AI and the Model Context Protocol (MCP).

## Architecture Overview

This project follows a client-server architecture with three main components:

### 1. Backend API Server (`mcp_server/server.py`)
- **Technology**: FastAPI (modern, fast web framework)
- **Purpose**: Provides structured access to Barbie movie data through MCP tools
- **Port**: Runs on http://localhost:8001
- **Key Endpoints**:
  - `/list_tools` (GET): Returns all available tools with descriptions
  - `/call_tool` (POST): Executes a specific tool with parameters

### 2. Frontend Chatbot (`app.py`)
- **Technology**: Terminal-based UI, Google Gemini AI
- **Purpose**: Provides interactive chat interface for users to ask questions
- **Features**:
  - Natural language processing
  - Automatic tool selection using AI
  - Response formatting
  - Error handling and recovery

### 3. API Client (`mcp_client/client.py`)
- **Technology**: Python requests library
- **Purpose**: Lightweight HTTP client for communicating with the MCP server
- **Functions**:
  - `list_tools()`: Retrieves available tools from server
  - `call_tool(name, args)`: Executes a specific tool with parameters

### 4. Configuration (`ai_config.py`)
- **Purpose**: Centralized configuration for AI service
- **Content**:
  - `GEMINI_API_KEY`: API key for Google's Gemini service
  - `GEMINI_MODEL`: Specifies the AI model to use (currently "gemma-3-27b-it")

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Google Cloud account with Gemini API access

### Installation
1. Install dependencies:
   ```bash
   pip install fastapi uvicorn google-generativeai python-multipart requests
   ```

2. (Optional) Set up environment variables:
   ```bash
   # For Windows
   set GEMINI_API_KEY="your-api-key-here"

   # For macOS/Linux
   export GEMINI_API_KEY="your-api-key-here"
   ```

## Running the Application

### Start the Backend Server
```bash
cd barbie-mcp/mcp_server
uvicorn server:app --reload --port 8001
```

### Run the Chatbot
```bash
cd barbie-mcp
python app.py
```

## Usage

Once the application is running, you'll see an interactive chat interface. You can ask questions like:

### Example Queries
- "List all Barbie movies"
- "What's the plot of Barbie: Princess Charm School?"
- "Which Barbie movie features a mermaid?"
- "Find Barbie movies about fashion"
- "Give me a random Barbie movie"

### Available Tools
The chatbot can use the following tools:

1. **list_barbie_movies**: Returns all Barbie movies with detailed information
2. **search_movies**: Finds movies by keyword in title or summary
3. **filter_movies**: Filters movies by minimum IMDb rating and duration
4. **get_movie_details**: Provides comprehensive details about a specific movie
5. **random_barbie_movie**: Returns a randomly selected Barbie movie

## Project Structure

```
barbie-mcp/
├── app.py                          # Frontend chatbot application
├── ai_config.py                    # AI service configuration
├── mcp_client/
│   └── client.py                  # API client for server communication
└── mcp_server/
    └── server.py                  # Backend API server
```

## Configuration Details

### AI Configuration (`ai_config.py`)
```python
import os

# Shared Gemini configuration for app + MCP server.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyD01IpzCva2Ck1DOOFXV6X3ND3vSTUgg_M"
GEMINI_MODEL = "gemma-3-27b-it"
```

- **API Key Management**: Falls back to a default API key if environment variable not set
- **Model Selection**: Currently using "gemma-3-27b-it" for high-quality responses

## How It Works

### Query Processing Flow
1. **User Input**: User asks a question about Barbie movies
2. **Tool Detection**: App uses Gemini to determine if query asks for tool list
3. **AI Decision Making**: If tool list is requested, app responds with available tools
4. **Tool Selection**: For data queries, app uses Gemini to select appropriate tool
5. **Tool Execution**: App calls backend server to execute selected tool
6. **Response Formatting**: App uses Gemini to format tool output into natural language
7. **User Display**: Final answer is presented to the user

### Server Operation
- Server receives tool execution requests
- Each tool uses Google Gemini to retrieve accurate Barbie movie information
- Results are returned as JSON data to the app
- Server handles 5 specific Barbie movie information tools

## Troubleshooting

### Common Issues

1. **API Connection Errors**:
   - Ensure backend server is running on port 8001
   - Check firewall settings
   - Verify MCP server URL in `mcp_client/client.py`

2. **API Key Issues**:
   - Check environment variable is set correctly
   - Verify API key has Gemini API permissions
   - Test key using Google Cloud Console

3. **AI Response Errors**:
   - Check internet connectivity
   - Verify API key validity
   - Review error messages for specific Gemini API issues

## Extending the Application

### Adding New Tools
1. Define new tool in `mcp_server/server.py`
2. Update the `list_tools()` function with tool information
3. Add handling in the `call_tool()` function
4. Create a new prompt for the AI to retrieve data using Gemini

### Modifying AI Behavior
1. Adjust prompts in `app.py` and `mcp_server/server.py`
2. Change model in `ai_config.py`
3. Modify response formatting logic in `app.py`

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is for educational and demonstration purposes. Please respect Google's AI usage policies and terms of service.