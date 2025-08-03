# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

def main():
    # Start the MCP server
    mcp.run(host="server", port=8000, debug=True)
if __name__ == "__main__":
    main() 
# This code sets up a simple MCP server with an addition tool and a dynamic greeting resource.