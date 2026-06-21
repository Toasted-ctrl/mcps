from prometheus_client import start_http_server

from .config import config
from .server import mcp
from .tools.database.get_database_names import get_database_names
from .tools.tables.get_table_details import get_table_details
from .tools.tables.get_table_names import get_table_names


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