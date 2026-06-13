from prometheus_client import start_http_server

from .config import config
from .server import mcp
from .tools.ge.get_grand_exchange_item import get_grand_exchange_item
from .tools.hiscore.disable_player_tracking import disable_player_tracking
from .tools.hiscore.get_player_current_hiscore import get_player_current_hiscore
from .tools.hiscore.get_player_historical_hiscore_item import get_player_historical_hiscore_item
from .tools.hiscore.get_players_tracked_hiscores import get_players_tracked_hiscores
from .tools.hiscore.post_tracked_user import post_tracked_user

from shared.logger import get_logger

if __name__ == "__main__":
    log = get_logger(name=config.MCP_NAME)
    log.info(f"Starting Prometheus endpoint at port {config.PROMETHEUS_PORT}")
    
    start_http_server(
        port=config.PROMETHEUS_PORT,
        addr="0.0.0.0"
    )

    log.info(f"Starting {config.MCP_NAME} at port {config.MCP_PORT}")
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=config.MCP_PORT,
        path="/mcp"
    )