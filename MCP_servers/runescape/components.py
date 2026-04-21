import os
import requests

from dotenv import load_dotenv

from unpack_hiscore import unpack_hiscore # NOTE: Double check if this works in prod.

load_dotenv()

def get_player_hiscore(player_name: str) -> dict:
    if player_name == "":
        raise ValueError("Player name must not be None")
    url = os.getenv(key="RUNESCAPE_HISCORE_URL")
    params = {"player": player_name}
    try:
        request = requests.get(url=url, params=params)
        request.raise_for_status()
        return {
            "message": "Success",
            "detail": unpack_hiscore(input=str(request.text))
        }
    except requests.exceptions.ConnectionError:
        return {
            "error": "connection_error",
            "message": "MCP server has no internet access"
        }
    except requests.exceptions.HTTPError:
        return {
            "error": "http_error",
            "message": "Could not connect to RuneScape's hiscore services"
        }
    except ValueError as verr:
        return {
            "error": "ValueError",
            "messages": verr
        }