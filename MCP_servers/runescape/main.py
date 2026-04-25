from fastmcp import FastMCP

from components import get_player_hiscore

mcp = FastMCP(
    name="RuneScape")

@mcp.tool()
def get_runescape_player_current_hiscore(
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

if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=8000)