import os
import requests

from dotenv import load_dotenv

from unpack_hiscore import unpack_hiscore

load_dotenv()

def get_player_hiscore(player_name: str) -> dict:
    try:
        if player_name == "":
            raise ValueError("Player name must not be None")
        
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
    
    except ValueError as err:
        return {
            "error": "ValueError",
            "message": str(err)
        }
    
def get_grand_exchange_item_id(item_id: int) -> dict:
    try:
        if not item_id:
            raise ValueError("Missing item_id")
        
        url = os.getenv("RUNESCAPE_GE_ITEM_ID")
        params = {"item": item_id}
        response = requests.get(url=url, params=params)
        response.raise_for_status()
        return {
            "message": "Success",
            "item": response.json().get('item')
        }
    
    except requests.exceptions.ConnectionError:
        return {
            "error": "connection_error",
            "message": "MCP server has no internet access"
        }
    
    except requests.exceptions.HTTPError:
        return {
            "error": "http_error",
            "message": "Could not connect to RuneScape's Grand Exchange services"
        }
        
    except ValueError as err:
        return {
            "error": "ValueError",
            "message": str(err)
        }