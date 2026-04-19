import os
import requests

from dotenv import load_dotenv

load_dotenv()

def get_player_hiscore(player_name: str) -> dict:
    url = os.getenv(key="RUNESCAPE_HISCORE_URL")
    params = {"player": player_name}
    try:
        request = requests.get(url=url, params=params)
        request.raise_for_status()
        return {
            "detail": str(request.text())   # TODO: Rework this so we have all the proper formatting
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