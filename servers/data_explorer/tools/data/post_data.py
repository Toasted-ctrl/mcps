from pydantic import Field, BaseModel
from typing import Annotated
import requests

from ...config import config
from ...server import mcp

from shared.logger import get_logger

log = get_logger(name=config.MCP_NAME)

class Source(BaseModel):
    description: str = Field(description="High level description of the source")
    base_url: str = Field(description="Base URL of the source. Example: http://randomsite.com")
    url_ext: str | None = Field(default=None, description="Extension of the URL. Example: /extension-url")
    params: dict | None = Field(default=None, description="Parameters required for each source request")
    content_type: str = Field(description="Request content type. Example: 'application/json', 'text/html'")
    sequence: str = Field(description="Interval at which the source needs to be mined. Example: 'hourly', '30 minute interval'")
    headers: dict | None = Field(default=None, description="Headers required for each request")

@mcp.tool(
    name="post_data_ingest_sources",
    version="0.0.1",
    description="Adds a new source to the ingest_sources table.",
    meta={
        "author": "Toasted-ctrl"
    }
)
def post_data_ingest_sources(
    data: Annotated[Source, Field(description="The source object to be added to the ingest_sources table.")]
) -> dict:
    url = config.DIA_URL_BASE + config.DIA_URL_SOURCES
    log.debug(f"URL: {url}")
    response = requests.post(url=url, json=data.model_dump())
    response.raise_for_status()
    return {
        "new_source": data
    }

    # TODO: Rework to not just test, but add proper headers etc.
    # TODO: Errors out, need to debug. Something with the url is blocking.