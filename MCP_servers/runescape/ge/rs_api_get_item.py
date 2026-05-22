import os
import requests

from dotenv import load_dotenv

def get_grand_exchange_item_id(item_id: int) -> dict:
    try:
        if not item_id:
            raise ValueError("Missing item_id")
        load_dotenv()
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