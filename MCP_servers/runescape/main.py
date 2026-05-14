from fastmcp import FastMCP

from components import get_player_hiscore, get_grand_exchange_item_id
from tracked_hiscores import get_tracked_hs_users

mcp = FastMCP(
    name="RuneScape MCP")

@mcp.tool(
    name="get_runescape_player_current_hiscore",
    version="1.0.0",
    meta={
        "author": "Toasted-ctrl"
    },

)
def get_current_hiscore(
    player_name: str
) -> dict:
    """Retrieves and returns the current hiscore listings for the specified RuneScape player.
    
    Only use this tool when the user is asking for the hiscores or stats of a RuneScape player.
    A specific player's name (player_name) must be specified.

    Do NOT use this tool if the user asks any other question.

    Do NOT provide any arguments besides the player_name.

    Returns:
    - A dictionary of stats / hiscores related to the specified RuneScape player."""

    return get_player_hiscore(player_name=player_name)

@mcp.tool(
    name="get_runescape_grand_exchange_item",
    version="0.1.0",
    meta={
        "author": "Toasted-ctrl"
    }
)
def get_grand_exchange_item(
    item_id: int
) -> dict:

    """Retrieves Grand Exhange information for an item that can be sold on the Grand Exchange.
    
    Only use this tool when the user is asking for sales data with an item id, or asking for Grand Exchange data on an item id.
    If the user does not specify an item id, you may ask for one.
    
    Do NOT use this tool for hiscore related queries.
    
    Do NOT provide any arguments besides the item_id.
    
    Returns a dictionary which includes:
    - The item type: str
    - The item id: int
    - The item name: str
    - The item description: str
    - Whether the item is a member's item: boolean
    - The prcinging trends (trend, price, an optionally change if 30 days or more):
        - Current
        - Today
        - day30
        - day90
        - day180"""

    return get_grand_exchange_item_id(item_id=item_id)

@mcp.tool(
    name="get_runescape_tracked_hiscore_players",
    version="0.1.0",
    meta={
        "author": "Toasted-ctrl"
    }
)
def get_tracked_hiscore_players() -> dict:
    
    """Retrieves a list of players / usernames for which currently historical hiscore data is being tracked.
    
    Only use this tool when the user is asking for information on who / what player / what user is being tracked when it regards hiscores.
    
    Do NOT provide any arguments for this tool.
    
    Returns:
    - List of usernames: str"""

    try:
        users: list = get_tracked_hs_users()
        return {
            "tracked_users_hiscores": users
        }
    
    except Exception as e:
        print(e)
        return {
            "error": "Unexpected error"
        }

if __name__ == "__main__":

    # TODO: find out why we there are issues with "streamable-http"

    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=8000)