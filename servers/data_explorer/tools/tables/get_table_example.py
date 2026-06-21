from pydantic import Field
from sqlalchemy import create_engine, MetaData, Table, select
from typing import Annotated

from ...config import config
from ...server import mcp

from shared.errors import NotFoundError
from shared.logger import get_logger

log = get_logger(name=config.MCP_NAME)

@mcp.tool(
    name="get_table_example",
    version="0.0.1",
    description="Retrieves data from the first 5 rows from a table.",
    meta={
        "author": "Toasted-ctrl"
    }
)
def get_table_example(
    database: Annotated[str, Field(description="Database name")],
    table: Annotated[str, Field(description="Table name")]
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
        t = Table(table, metadata, autoload_with=engine)
        with engine.connect() as conn:
            log.debug(f"Connected to database '{database}'")
            result = conn.execute(select(t).limit(5))
            rows = result.fetchall()
        if not rows:
            raise NotFoundError("Empty table")
        return {
            "database": database,
            "table": table,
            "rows": [row._asdict() for row in rows]
        }
    finally:
        engine.dispose()
        log.debug("Disposed engine")