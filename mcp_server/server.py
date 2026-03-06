from fastapi import FastAPI
import json
from google import genai

try:
    from ai_config import GEMINI_API_KEY, GEMINI_MODEL
except ModuleNotFoundError:
    import os
    import sys

    # Allow running from mcp_server/ as current working directory.
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from ai_config import GEMINI_API_KEY, GEMINI_MODEL

app = FastAPI()

ai_client = genai.Client(api_key=GEMINI_API_KEY)


def ask_gemini(prompt):
    response = ai_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )
    text = response.text.strip()
    if text.startswith("```"):
        if "json" in text[:10]:
            text = text.split("```json")[1].split("```")[0].strip()
        else:
            text = text.split("```")[1].strip()
    return json.loads(text)


@app.get("/list_tools")
def list_tools():
    return [
        {
            "name": "list_barbie_movies",
            "description": "Return all Barbie movies"
        },
        {
            "name": "search_movies",
            "description": "Find Barbie movies by keyword in summary or title",
            "parameters": ["query"]
        },
        {
            "name": "filter_movies",
            "description": "Filter movies by rating and duration",
            "parameters": ["min_rating", "min_duration_minutes"]
        },
        {
            "name": "get_movie_details",
            "description": "Return details for a movie",
            "parameters": ["title"]
        },
        {
            "name": "random_barbie_movie",
            "description": "Return a random Barbie movie"
        }
    ]


@app.post("/call_tool")
def call_tool(data: dict):
    tool_name = data.get("tool_name")
    args = data.get("args", {})

    if tool_name == "list_barbie_movies":
        return ask_gemini(
            "List all Barbie animated movies with their title, year, duration, "
            "imdb_rating, director, stars, and a short summary. "
            "Return ONLY a JSON array of objects. No extra text."
        )

    if tool_name == "search_movies":
        query = args.get("query", "")
        return ask_gemini(
            f'Search for Barbie movies related to "{query}". '
            "Return ONLY a JSON array of matching movies with title, year, duration, "
            "imdb_rating, director, stars, and summary. No extra text."
        )

    if tool_name == "filter_movies":
        min_rating = args.get("min_rating", 0)
        min_duration = args.get("min_duration_minutes", 0)
        return ask_gemini(
            f"List Barbie movies with an IMDb rating of at least {min_rating} "
            f"and a duration of at least {min_duration} minutes. "
            "Return ONLY a JSON array with title, year, duration, imdb_rating, "
            "director, stars, and summary. No extra text."
        )

    if tool_name == "get_movie_details":
        title = args.get("title", "")
        return ask_gemini(
            f'Give full details about the Barbie movie titled "{title}". '
            "Return ONLY a JSON object with title, year, duration, rating, "
            "imdb_rating, director, stars, and summary. No extra text."
        )

    if tool_name == "random_barbie_movie":
        return ask_gemini(
            "Pick one random Barbie movie and return ONLY a JSON object with "
            "title, year, duration, imdb_rating, director, stars, and summary. No extra text."
        )

    return {"error": "Unknown tool"}
