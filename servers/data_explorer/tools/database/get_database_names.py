from ...config import config
from ...server import mcp

@mcp.tool(
    name="get_database_names",
    version="0.0.1",
    description="Retrieves a list of all accessible databases",
    meta={
        "author": "Toasted-ctrl"
    }
)
def get_database_names() -> dict:
    return {
        "databases": config.DB_DATABASES
    }