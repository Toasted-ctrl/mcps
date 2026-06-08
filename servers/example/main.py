from prometheus_client import start_http_server

from .config import config
from .server import mcp

from shared.logger import get_logger

if __name__ == "__main__":
    log = get_logger()
    log.info(f"Starting Prometheus endpoint at port {config.PROMETHEUS_PORT}")
    
    start_http_server(
        port=config.PROMETHEUS_PORT,
        addr="0.0.0.0"
    )

    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=config.MCP_PORT,
        path="/mcp"
    )