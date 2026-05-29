from fastmcp import FastMCP
from prometheus_client import start_http_server, Counter, Histogram
from pydantic import Field
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated, Optional
import functools

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

log = get_logger()

def metrics_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        fname = func.__name__
        TOOL_CALLS.labels(tool_name=fname).inc()
        with TOOL_DURATION.labels(tool_name=fname).time():
            try:
                log.info(f"Calling {fname} with args={args}, kwargs={kwargs}")
                return func(*args, **kwargs)
            except ValueError as e:
                TOOL_ERRORS.labels(tool_name=fname).inc()
                log.error(str(e))
                raise Exception(str(e)) from e
            except SQLAlchemyError as e:
                TOOL_ERRORS.labels(tool_name=fname).inc()
                log.error(e)
                raise Exception("A database error occurred. Check server logs for details.") from e
            except NotFoundError as e:
                TOOL_ERRORS.labels(tool_name=fname).inc()
                log.info(e)
                raise Exception(str(e)) from e
            except Exception as e:
                TOOL_ERRORS.labels(tool_name=fname).inc()
                log.error(str(e))
                raise Exception("An unexpected error occured. Check server logs for details.") from e
    return wrapper

mcp = FastMCP(
    name="RuneScape MCP")

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
@metrics_handler
def get_current_hiscore(
    player_name: Annotated[str, Field(description="Name of the RuneScape player.")]
) -> dict:
        log.info(f"Args: player_name = '{player_name}'")
        return get_player_hiscore(player_name=player_name)

@mcp.tool(
    name="get_runescape_grand_exchange_item",
    version="0.1.0",
    meta={
        "author": "Toasted-ctrl"
    },
    description=(
        "Retrieves Grand Exhange information for an item that can be sold on the Grand Exchange. "
        "Only use this tool when the user is asking for sales data with an item id, or asking for Grand Exchange data on an item id. "
        "If the user does not specify an item id, you may ask for one. "
        "Do NOT use this tool for hiscore related queries. "
        "Returns a dictionary which includes: "
        "item type, item id, item name, item description, item member status, pricing trends: (current, today, day30, day90, day180)."
    )
)
@metrics_handler
def get_grand_exchange_item(
    item_id: Annotated[int, Field(description="Integer representing the id of the item.")]
) -> dict:
    log.info(f"Args: item_id = '{item_id}'")
    return get_grand_exchange_item_id(item_id=item_id)

@mcp.tool(
    name="get_runescape_tracked_hiscore_players",
    version="0.1.0",
    meta={
        "author": "Toasted-ctrl"
    },
    description=(
        "Retrieves a list of players / usernames for which currently historical hiscore data is being tracked. "
        "Only use this tool when the user is asking for information on who / what player / what user is being tracked when it regards hiscores. "
        "Returns: a list of tracked usernames."
    )
)
@metrics_handler
def get_tracked_hiscore_players() -> dict:
    log.info("Args: None")
    return {
        "tracked_users_hiscores": get_tracked_hs_users()
    }
    
@mcp.tool(
    name="post_runescape_tracked_users",
    version="0.1.1",
    meta={
        "author": "Toasted-ctrl"
    },
    description=(
        "Adds a new user / username / player_name for which hiscores / stats / runemetrics profiles need to be tracked. "
        "Only use this tool when the user is requesting to add tracking a player / user. "
        "Returns the player_name if added successfully."
    )
)
@metrics_handler
def post_track_user(
    player_name: Annotated[str, Field(description="Name of the RuneScape player.")]
) -> dict[str, str]:
    log.info(f"Args: player_name = '{player_name}'")
    return {
        "tracking_enabled": post_tracked_user(player_name=player_name),
    }
    
@mcp.tool(
    name="disable_runescape_tracked_user",
    version="0.1.0",
    meta={
        "author": "Toasted-ctrl"
    },
    description=(
        "This function disables tracking for a RuneScape player, if the player is CURRENTLY actively being tracked. "
        "Returns the player_name if tracking was successfully disabled. "
        "Will return an error if the player's tracking is already disabled, "
        "or if the player does not exist in the tracking database."
    )
)
@metrics_handler
def disable_tracking_user(
    player_name: Annotated[str, Field(description="Name of the RuneScape player.")]
) -> dict[str, str]:
    log.info(f"Args: player_name = '{player_name}'")
    return {
        "tracking_disabled": disable_tracking(player_name=player_name)
    }
    
@mcp.tool(
    name="get_runescape_player_historical_hiscore_item",
    version="0.1.0",
    meta={
        "author": "Toasted-ctrl"
    },
    description=(
        "Only use this function to fetch historical records for a skill or activity for a tracked player. "
        "If records are stored, a dictionary with the player records will be returned. "
        "The returned dict is based on the first found date FROM the indicated date and time."
    )
)
@metrics_handler
def get_runescape_player_historical_hiscore_item(
    player_name: Annotated[str, Field(description="Name of the RuneScape player.")],
    skill_or_activity: Annotated[str, Field(description="The activity or skill for which the player's stats need to be retrieved.")],
    date: Annotated[Optional[str], Field(description="Earliest date for which the record needs to be retrieved, example: '2026-05-11' (yyyy-mm-dd).")] = None,
    time: Annotated[Optional[str], Field(description="Earliest time for which the record needs to be retrieved, example: '13:11'.")] = None
) -> dict:
    return {
        "player_name": player_name,
        "historical_record": get_user_historical_hs_item(
            player_name=player_name,
            skill_or_activity=skill_or_activity,
            date=date,
            time=time
        )
    }

if __name__ == "__main__":
    log.info("Starting Prometheus endpoint")
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