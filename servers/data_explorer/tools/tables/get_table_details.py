from pydantic import Field
from sqlalchemy import create_engine, MetaData
from typing import Annotated

from ...config import config
from ...server import mcp

from shared.logger import get_logger

log = get_logger(name=config.MCP_NAME)

@mcp.tool(
    name="get_table_details",
    version="0.0.1",
    description="Retrieves table information for a specific table.",
    meta={
        "author": "Toasted-ctrl"
    }
)
def get_table_details(
    database: Annotated[str, Field(description="Name of database")],
    table: Annotated[str, Field(description="Name of table")]
) -> dict:
    if not database or not table:
        raise ValueError("Database and table must not be null")
    if not database in config.DB_DATABASES:
        raise ValueError(f"Database '{database}' does not exist")
    db_url = config.db_url(db_database=database)
    try:
        engine = create_engine(url=db_url)
        log.debug("Created engine")
        metadata = MetaData()
        metadata.reflect(bind=engine)
        tables = metadata.tables.items()
        for name, obj in tables:
            if name == table:
                return {
                    "database": database,
                    "table": table,
                    "table_schema": [
                        {
                            "column_name": col.name,
                            "type": str(col.type),
                            "nullable": col.nullable,
                            "primary_key": col.primary_key
                        }
                        for col in obj.columns
                    ]
                }
        raise ValueError(f"Table '{table}' nonexistant in database '{database}'")
    finally:
        engine.dispose()
        log.debug("Disposed engine")