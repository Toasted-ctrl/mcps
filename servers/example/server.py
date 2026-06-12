from fastmcp import FastMCP
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.server.middleware.logging import LoggingMiddleware

from .config import config

from shared.prometheus import PrometheusMiddleware

mcp = FastMCP(
    name=config.MCP_NAME
)

mcp.add_middleware(LoggingMiddleware(
    include_payloads=True
))

mcp.add_middleware(ErrorHandlingMiddleware(
    include_traceback=True,
    transform_errors=True
))

mcp.add_middleware(PrometheusMiddleware())

