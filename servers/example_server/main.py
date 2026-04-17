from fastapi import FastAPI
from fastmcp import FastMCP

mcp = FastMCP("Example MCP")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

app = FastAPI()
app.mount("/mcp", mcp.asgi_app())