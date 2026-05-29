import os
import requests

from dotenv import load_dotenv

from hiscore.unpack_hiscore import unpack_hiscore

def get_player_hiscore(player_name: str) -> dict:
    try:
        if player_name == "":
            raise ValueError("Player name must not be None")
        load_dotenv()
        url = os.getenv(key="RUNESCAPE_HISCORE_URL")
        params = {"player": player_name}
        response = requests.get(url=url, params=params)
        response.raise_for_status()
        return {
            "message": "Success",
            "detail": unpack_hiscore(input=str(response.text))
        }
    
    except requests.exceptions.ConnectionError:
        return {
            "error": "connection_error",
            "message": "MCP server has no internet access"
        }
    
    except requests.exceptions.HTTPError:
        return {
            "error": "http_error",
            "message": "Could not connect to RuneScape's Hiscore services"
        }
    
