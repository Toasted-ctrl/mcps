from fastmcp import FastMCP
from prometheus_client import start_http_server, Counter, Histogram
from pydantic import Field
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated, Optional
import sys

from core.logger import get_logger
from db.errors import NotFoundError
from ge.rs_api_get_item import get_grand_exchange_item_id
from hiscore.rs_api_get_hiscore import get_player_hiscore

from hiscore.tracked_hiscores import (
    get_tracked_hs_users,
    post_tracked_user,
    disable_tracking,
    get_user_historical_hs_item
)

TOOL_CALLS = Counter(
    "mcp_tool_calls_total", "Total tool invocations", ["tool_name"]
)

TOOL_DURATION = Histogram(
    "mcp_tool_duration_seconds", "Tool call duration in seconds", ["tool_name"]
)

TOOL_ERRORS = Counter(
    "mcp_tool_errors_total", "Total tool errors", ["tool_name"]
)

mcp = FastMCP(
    name="RuneScape MCP")

log = get_logger()

@mcp.tool(
    name="get_runescape_player_current_hiscore",
    version="1.0.1",
    meta={
        "author": "Toasted-ctrl"
    },
    description=(
        "Retrieves and returns the current hiscore listings for the specified RuneScape player. "
        "Only use this tool when the user is asking for the hiscores or stats of a RuneScape player. "
        "Do NOT use this tool if the user asks any other question. "
        "Returns a dictionary of stats / hiscores related to the specified RuneScape player."
    )
)
def get_current_hiscore(
    player_name: Annotated[str, Field(description="Name of the RuneScape player.")]
) -> dict:
    fname = sys._getframe().f_code.co_name
    TOOL_CALLS.labels(tool_name=fname).inc()
    with TOOL_DURATION.labels(tool_name=fname).time():
        try:
            log.info(f"Args: player_name = '{player_name}'")
            return get_player_hiscore(player_name=player_name)

        except Exception as e:
            TOOL_ERRORS.labels(tool_name=fname).inc()
            log.error(str(e))
            raise Exception("An unexpected error occurred. Check server logs for details.") from e
            #return {
                #"unexpected_error": "An unexpected error occurred. Check server logs for details."
            #}

@mcp.tool(
    name="get_runescape_grand_exchange_item",
    version="0.1.0",
    meta={
        "author": "Toasted-ctrl"
    }
)
def get_grand_exchange_item(
    item_id: Annotated[int, Field(description="Integer representing the id of the item.")]
) -> dict:

    """Retrieves Grand Exhange information for an item that can be sold on the Grand Exchange.
    
    Only use this tool when the user is asking for sales data with an item id, or asking for Grand Exchange data on an item id.
    If the user does not specify an item id, you may ask for one.
    
    Do NOT use this tool for hiscore related queries.
    
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
    try:
        log.info(f"Args: item_id = '{item_id}'")
        return get_grand_exchange_item_id(item_id=item_id)

    except Exception as e:
        log.error(str(e))
        return {
            "unexpected_error": "An unexpected error occurred. Check server logs for details."
        }

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
    Returns:
    - List of usernames: str"""

    try:
        log.info("Args: None")
        return {
            "tracked_users_hiscores": get_tracked_hs_users()
        }
    
    except SQLAlchemyError as e:
        log.error(str(e))
        return {
            "database_error": "A database error occurred. Check server logs for details."
        }

    except Exception as e:
        log.error(str(e))
        return {
            "unexpected_error": "An unexpected error occurred. Check server logs for details."
        }
    
@mcp.tool(
    name="post_runescape_tracked_users",
    version="0.1.1",
    meta={
        "author": "Toasted-ctrl"
    }
)
def post_track_user(
    player_name: Annotated[str, Field(description="Name of the RuneScape player.")]
) -> dict[str, str]:

    """Adds a new user / username / player_name for which hiscores / stats / runemetrics profiles need to be tracked.
    Only use this tool when the user is requesting to add tracking a player / user.
    Returns the player_name if added successfully."""

    try:
        log.info(f"Args: player_name = '{player_name}'")
        return {
            "tracking_enabled": post_tracked_user(player_name=player_name),
        }
    
    except ValueError as e:
        log.info(str(e))
        return {
            "value_error": str(e)
        }
    
    except SQLAlchemyError as e:
        log.error(str(e))
        return {
            "database_error": "A database error occurred. Check server logs for details."
        }

    except Exception as e:
        log.error(str(e))
        return {
            "unexpected_error": "An unexpected error occurred. Check server logs for details."
        }
    
@mcp.tool(
    name="disable_runescape_tracked_user",
    version="0.1.0",
    meta={
        "author": "Toasted-ctrl"
    }
)
def disable_tracking_user(
    player_name: Annotated[str, Field(description="Name of the RuneScape player.")]
) -> dict[str, str]:
    
    """This function disables tracking for a RuneScape player, if the player is CURRENTLY actively being tracked.
    Returns the player_name if tracking was successfully disabled.
    Will return an error if the player's tracking is already disabled,
    or if the player does not exist in the tracking database."""

    try:
        log.info(f"Args: player_name = '{player_name}'")
        return {
            "tracking_disabled": disable_tracking(player_name=player_name)
        }
    
    except NotFoundError as e:
        log.info(str(e))
        return {
            "not_found_error": str(e)
        }
    
    except SQLAlchemyError as e:
        log.error(str(e))
        return {
            "database_error": "A database error occurred. Check server logs for details."
        }
    
    except Exception as e:
        log.error(str(e))
        return {
            "unexpected_error": "An unexpected error occurred. Check server logs for details."
        }
    
@mcp.tool(
    name="get_runescape_player_historical_hiscore_item",
    version="0.1.0",
    meta={
        "author": "Toasted-ctrl"
    }
)
def get_runescape_player_historical_hiscore_item(
    player_name: Annotated[str, Field(description="Name of the RuneScape player.")],
    skill_or_activity: Annotated[str, Field(description="The activity or skill for which the player's stats need to be retrieved.")],
    date: Annotated[Optional[str], Field(description="Earliest date for which the record needs to be retrieved, example: '2026-05-11' (yyyy-mm-dd).")] = None,
    time: Annotated[Optional[str], Field(description="Earliest time for which the record needs to be retrieved, example: '13:11'.")] = None
) -> dict:
    
    """Only use this function to fetch historical records for a skill or activity for a tracked player.
    If records are stored, a dictionary with the player records will be returned.
    The returned dict is based on the first found date FROM the indicated min_date."""
    
    try:
        return {
            "player_name": player_name,
            "historical_record": get_user_historical_hs_item(
                player_name=player_name,
                skill_or_activity=skill_or_activity,
                date=date,
                time=time
            )
        }
    
    except NotFoundError as e:
        log.info(str(e))
        return {
            "not_found_error": str(e)
        }
    
    except SQLAlchemyError as e:
        log.error(str(e))
        return {
            "database_error": "A database error occurred. Check server logs for details."
        }
    
    except Exception as e:
        log.error(str(e))
        return {
            "unexpected_error": "An unexpected error occurred. Check server logs for details."
        }

if __name__ == "__main__":
    log.info("Starting Prometheus server")
    start_http_server(
        port=8989,
        addr="0.0.0.0"
    )

    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
        path="/mcp"
    )