from fastmcp.server.middleware import Middleware

class UserFacingError(Exception):
    pass

SAFE_EXCEPTIONS: tuple[type[Exception], ...] = (
    UserFacingError,
    ValueError,
    TypeError,
    KeyError,
    NotImplementedError
)

GENERIC_MESSAGE = "An internal error occured. Please try again later."

class SanitizedErrorMiddleware(Middleware):

    """
    Sits between ErrorHandlingMiddleware and tool execution.
    
    - Exceptions in SAFE_EXCEPTIONS pass through unchanged.
    - Everything else is replaced with a generic RuntimeError
    so that database details, file paths, hostnames, etc.
    never reach the client.
    """

    def __init__(
        self,
        *,
        generic_message: str = GENERIC_MESSAGE,
        safe_exceptions: tuple[type[Exception], ...] | None = None
    ):
        self.generic_message = generic_message
        self.safe_exceptions = safe_exceptions or SAFE_EXCEPTIONS

    async def on_call_tool(self, request, call_next):
        return await self._safe_call(call_next, request)
    
    async def _safe_call(self, call_next, request):
        try:
            return await call_next(request)
        except self.safe_exceptions:
            raise
        except Exception:
            raise RuntimeError(self.generic_message) from None