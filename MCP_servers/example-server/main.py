from fastmcp import FastMCP
from prometheus_client import start_http_server
import sys

from logger.logger import get_logger
from prometheus.metrics_handler import metrics_handler

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
    log.info(f"Calling '{sys._getframe().f_code.co_name}' with args: {num_1}, {num_2}")
    return {
        "answer": num_1 + num_2
    }

if __name__ == "__main__":
    log.info("Starting Prometheus endpoint")
    start_http_server(
        port=8787,
        addr="0.0.0.0"
    )
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
        path="/mcp"
    )