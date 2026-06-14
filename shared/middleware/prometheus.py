from fastmcp.server.middleware import Middleware
from prometheus_client import Counter, Histogram
import time

TOOL_CALLS = Counter(
    "mcp_tool_calls_total",
    "Tool invocations",
    ["tool", "status"],
)

TOOL_DURATION = Histogram(
    "mcp_tool_duration_seconds",
    "Tool execution time",
    ["tool"],
)

class PrometheusMiddleware(Middleware):
    async def on_call_tool(self, context, call_next):
        tool = context.message.name
        start = time.perf_counter()
        try:
            result = await call_next(context)

            TOOL_CALLS.labels(
                tool=tool,
                status="success",
            ).inc()

            return result

        except Exception:
            TOOL_CALLS.labels(
                tool=tool,
                status="error",
            ).inc()

            raise

        finally:
            TOOL_DURATION.labels(
                tool=tool,
            ).observe(
                time.perf_counter() - start
            )