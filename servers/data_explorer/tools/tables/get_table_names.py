from pydantic import Field
from sqlalchemy import create_engine, MetaData
from typing import Annotated

from ...config import config
from ...server import mcp

from shared.logger import get_logger

log = get_logger(name=config.MCP_NAME)

@mcp.tool(
    name="get_table_names",
    version="0.0.1",
    description="Gets a list of all available table names within a specified database.",
    meta={
        "author": "Toasted-ctrl"
    }
)
def get_table_names(
    database_name: Annotated[str, Field(description="Name of database to inspect")]
) -> dict:
    if not database_name:
        raise ValueError("Database must be defined")
    if not database_name in config.DB_DATABASES:
        raise ValueError("Nonexistant database")
    db_url = config.db_url(db_database=database_name)
    try:
        engine = create_engine(url=db_url)
        log.debug("Created engine")
        metadata = MetaData()
        metadata.reflect(bind=engine)
        tables = metadata.tables.keys()
        return {
            "database": database_name,
            "tables": list(tables)
        }
    finally:
        engine.dispose()
        log.debug("Disposed engine")