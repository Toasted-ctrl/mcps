from fastmcp import FastMCP
from prometheus_client import start_http_server
import sys

from core.config import config
from core.logger import get_logger
from core.prometheus import metrics_handler

# NOTE: Add @metrics_handler above every function, after @mcp.tool, to fetch performance data to expose on the prometheus endpoint.
# NOTE: @metrics_handler also handles exceptions.

log = get_logger()

mcp = FastMCP(
    name="Example MCP"
)

@mcp.tool(
    name="test_function_add",
    description="Adds two numbers"
)
@metrics_handler
def add(num_1: int, num_2: int) -> dict[str, int]:
    return {
        "answer": num_1 + num_2
    }

if __name__ == "__main__":
    if config.PROMETHEUS_PORT is None:
        sys.exit("Missing Prometheus port configuration")
    if config.MCP_PORT is None:
        sys.exit("Missing MCP port configuration")

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