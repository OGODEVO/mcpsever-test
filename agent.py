
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

# The URL of the running Playwright MCP server
SERVER_URL = "http://localhost:5051/sse"

async def main():
    """
    Connects to the MCP server and lists the available tools.
    """
    print(f"Connecting to MCP server at {SERVER_URL}...")

    try:
        # streamablehttp_client handles the SSE connection
        async with streamablehttp_client(SERVER_URL) as (read, write, _):
            # ClientSession manages the MCP protocol on top of the connection
            async with ClientSession(read, write) as session:
                print("Connection successful. Fetching tools...")

                # list_tools() is a standard MCP command
                tools = await session.list_tools()

                print("\nAvailable Tools:")
                if not tools:
                    print("- No tools found.")
                else:
                    for tool in tools:
                        # Print the name and description of each tool
                        print(f"- {tool.name}: {tool.description}")

    except ConnectionRefusedError:
        print(f"Connection failed. Is the server running at {SERVER_URL}?")
    except asyncio.CancelledError:
        print("The connection was cancelled.")
    except Exception as e:
        import traceback
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

