import os

# Shared Gemini configuration for app + MCP server.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "insert_your_api_key_here"
GEMINI_MODEL = "gemma-3-27b-it"
