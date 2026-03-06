import re
import json
from google import genai
from mcp_client.client import list_tools, call_tool
from ai_config import GEMINI_API_KEY, GEMINI_MODEL

# Initialize the Gemini client
# You can set the API key directly here if not using environment variables
ai_client = genai.Client(api_key=GEMINI_API_KEY)

def format_server_response(tool_name, answer_text):
    return f"[TOOL USED]: {tool_name}\nMY SERVER : {answer_text}\n-------------"

def is_tool_list_query(query):
    q = query.lower()
    return any(k in q for k in ["list tools", "tools available", "what tools", "available tools", "which tools"])

def format_available_tools(tools):
    lines = []
    for i, tool in enumerate(tools, start=1):
        name = tool.get("name", "unknown_tool")
        desc = tool.get("description", "Use this for related requests.")
        lines.append(f"{i}. {name}:")
        lines.append(f"          {desc}")
    return "\n".join(lines)

def extract_first_json_object(text):
    decoder = json.JSONDecoder()
    s = text.strip()

    # Try direct parse first.
    try:
        obj, _ = decoder.raw_decode(s)
        return obj
    except Exception:
        pass

    # Handle fenced output and fallback to first "{" occurrence.
    if s.startswith("```"):
        if "```json" in s:
            parts = s.split("```json", 1)
            if len(parts) > 1:
                s = parts[1].split("```", 1)[0].strip()
        else:
            parts = s.split("```", 2)
            if len(parts) > 1:
                s = parts[1].strip()

    start = s.find("{")
    if start == -1:
        raise ValueError("No JSON object found in model output.")

    obj, _ = decoder.raw_decode(s[start:])
    return obj

def handle_query(query):
    # 1. Get available tools
    tools_list = list_tools()

    if is_tool_list_query(query):
        return format_server_response("none", format_available_tools(tools_list))
    
    # 2. Tell the AI what tools are available and what the user wants
    prompt = f"""
    You are a helpful Barbie movie expert. You have access to the following MCP tools to answer the user's question:
    {json.dumps(tools_list, indent=2)}
    BASE RULE - DO NOT USE ANY MARKUP IN YOUR RESPONSES. ALWAYS RESPOND IN PLAIN TEXT.
    IF THE USER ASKS ANYTHING OTHER THAN BARBIE MOVIES, RESPOND WITH A POLITE MESSAGE SAYING YOU CAN ONLY HELP WITH BARBIE MOVIES ONLY.
    The user asked: "{query}"

    If the user asks for a list of tools or what tools are available, you should use the tools' names and descriptions provided above to answer.
    However, if the task requires actual data (like listing movies or searching), you must select and call the appropriate tool.

    Based on the tools above, determine which tool to call and with what arguments.
    Respond ONLY with a JSON object in this format:
    {{"tool_name": "name_of_tool", "args": {{"arg_name": "value"}}}}

    RESPOND TO THE TEXTS THAT HAS THE TOOLS DEFINED ONLY, ELSE PRINT "No appropriate tool found" IN THE EXPLANATION FIELD. DO NOT CALL ANY TOOL IF THE USER'S QUERY IS OUTSIDE THE SCOPE OF THE TOOLS DEFINED ABOVE. IN THAT CASE, RESPOND WITH {{"tool_name": "none", "explanation": "No appropriate tool found"}}.
    
    IMPORTANT: Respond ONLY with the JSON and one appropriate emoji and the ending of the answer. Do not include any other text, markdown formatting, or explanations outside the JSON.
    """

    response = ai_client.models.generate_content(
        model=GEMINI_MODEL, 
        contents=prompt
    )
    
    try:
        # Parse the AI's decision
        decision = extract_first_json_object(response.text)
    except Exception as e:
        # Fallback if the AI fails to produce clean JSON but has an explanation
        if '"explanation":' in response.text:
             try:
                 # Try to extract just the explanation if JSON parsing failed
                 explanation = response.text.split('"explanation": "')[1].split('"')[0].replace("\\n", "\n")
                 return format_server_response("none", explanation)
             except: pass
        return format_server_response("decision_error", f"AI Decision Error: {str(e)} - Raw: {response.text}")

    # 3. Execute the tool if one was selected
    if decision.get("tool_name") != "none":
        tool_result = call_tool(decision["tool_name"], decision.get("args", {}))
        
        # 4. Use the AI to format the final answer naturally
        format_prompt = f"""
        The user asked: "{query}"
        Relevant tool "{decision['tool_name']}" output:
        {json.dumps(tool_result, indent=2)}

        Provide a natural, helpful response based on the tool output only.
        Do not mention tool names, internal systems, or that a tool was used.
        Ensure you don't add any markups and always number the items if asked.
        """
        
        
        final_response = ai_client.models.generate_content(
            model=GEMINI_MODEL, 
            contents=format_prompt
        )
        return format_server_response(decision["tool_name"], final_response.text)
    else:
        return format_server_response("none", decision.get("explanation", "I'm not sure how to help with that."))


if __name__ == "__main__":
    startup_tools = list_tools()
    print(format_available_tools(startup_tools))
    print("-------------")

    while True:
        q = input("MCP SERVER: ")
        answer = handle_query(q)
        print(answer)
