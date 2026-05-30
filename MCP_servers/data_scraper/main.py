from fastmcp import FastMCP
from prometheus_client import start_http_server, Counter, Histogram
import functools

from core.logger import get_logger

TOOL_CALLS = Counter(
    "mcp_tool_calls_total", "Total tool invocations", ["tool_name"]
)

TOOL_DURATION = Histogram(
    "mcp_tool_duration_seconds", "Tool call duration in seconds", ["tool_name"]
)

TOOL_ERRORS = Counter(
    "mcp_tool_errors_total", "Total tool errors", ["tool_name"]
)

log = get_logger()

def metrics_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        fname = func.__name__
        TOOL_CALLS.labels(tool_name=fname).inc()
        with TOOL_DURATION.labels(tool_name=fname).time():
            try:
                log.info(f"Calling {fname} with args={args}, kwargs={kwargs}")
                return func(*args, **kwargs)
            except Exception as e:
                TOOL_ERRORS.labels(tool_name=fname).inc()
                log.error(str(e))
                raise Exception("An unexpected error occured. Check server logs for details.") from e
    return wrapper

mcp = FastMCP(
    name="Data Scraper MCP"
)

# TODO: Add base functions.

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