from pydantic import Field
from typing import Annotated
import requests

from shared.logger import get_logger
from shared.prometheus import metrics_handler
from ...server import mcp
from ...config import config

log = get_logger()

class GrandExchangeError(Exception):
    """Raised when errors with the grand exchange occur"""
    pass

def get_grand_exchange_item_id(item_id: int) -> dict:
    try:
        if not item_id:
            raise ValueError("Missing item_id")
        url = config.RS_GE_LINK
        params = {"item": item_id}
        response = requests.get(url=url, params=params)
        response.raise_for_status()
        return {
            "message": "Success",
            "item": response.json().get('item')
        }
    
    except requests.exceptions.HTTPError as e:
        log.info(str(e))
        return {
            "message": "Failed",
            "error": f"Could not retrieve item information for item {item_id}"
        }

@mcp.tool(
    name="get_runescape_grand_exchange_item",
    version="0.2.0",
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
    log.info(f"Args={locals()}")
    return get_grand_exchange_item_id(item_id=item_id)