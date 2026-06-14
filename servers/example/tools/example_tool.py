from pydantic import Field
from typing import Annotated

from ..server import mcp

@mcp.tool(
    name="sum_integers",
    version="1.0.0",
    description=("Example tool"),
    meta={
        "author": "Toasted-ctrl"
    }
)
def sum_integers(
    int_1: Annotated[int, Field(description="First integer")],
    int_2: Annotated[int, Field(description="Second integer")]
) -> dict:
    return {
        "result": int_1 + int_2
    }