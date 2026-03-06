import requests

MCP_SERVER = "http://localhost:8001"


def list_tools():
    r = requests.get(f"{MCP_SERVER}/list_tools")
    return r.json()


def call_tool(name, args={}):
    r = requests.post(
        f"{MCP_SERVER}/call_tool",
        json={"tool_name": name, "args": args}
    )
    return r.json() 