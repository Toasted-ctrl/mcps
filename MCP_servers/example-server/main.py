from dotenv import load_dotenv
from fastmcp import FastMCP
from prometheus_client import start_http_server
import os
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
    return {
        "answer": num_1 + num_2
    }

if __name__ == "__main__":
    log.info("Loading environment variables")
    load_dotenv()
    PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT"))
    if PROMETHEUS_PORT is None:
        sys.exit("Missing Prometheus port configuration")
    MCP_PORT = int(os.getenv("MCP_PORT"))
    if MCP_PORT is None:
        sys.exit("Missing MCP port configuration")

    log.info(f"Starting Prometheus endpoint at port {PROMETHEUS_PORT}")
    start_http_server(
        port=PROMETHEUS_PORT,
        addr="0.0.0.0"
    )
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=MCP_PORT,
        path="/mcp"
    )