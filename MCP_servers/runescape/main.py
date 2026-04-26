from fastmcp import FastMCP

from components import get_player_hiscore, get_grand_exchange_item_id

mcp = FastMCP(
    name="RuneScape MCP")

@mcp.tool(
    name="Get RuneScape Player Current Hiscore",
    version="1.0.0",
    meta={
        "author": "Toasted-ctrl"
    }
)
def get_current_hiscore(
    player_name: str
):
    """Retrieves and returns the current hiscore listings for the specified RuneScape player.
    
    Only use this tool when the user is asking for the hiscores or stats of a RuneScape player.
    A specific player's name (player_name) must be specified.

    Do NOT use this tool if the user asks any other question.

    Do NOT provide any arguments besides the player_name.

    Returns:
    - A dictionary of stats / hiscores related to the specified RuneScape player."""

    return get_player_hiscore(player_name=player_name)

@mcp.tool(
    name="Get RuneScape Grand Exchange Item",
    version="0.1.0",
    meta={
        "author": "Toasted-ctrl"
    }
)
def get_grand_exchange_item(
    item_id: int
):

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


if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=8000)