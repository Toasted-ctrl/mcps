from pydantic import Field
from typing import Annotated

from ...config import config
from ...db.schemas import ProdTrackedUsers
from ...server import mcp

from shared.db import get_db_session
from shared.errors import NotFoundError

@mcp.tool(
    name="disable_player_tracking",
    version="1.0.1",
    meta={
        "author": "Toasted-ctrl"
    },
    description=(
        "This function disables tracking for a RuneScape player, if the player is CURRENTLY actively being tracked. "
        "Returns the player_name if tracking was successfully disabled. "
        "Will return an error if the player's tracking is already disabled, "
        "or if the player does not exist in the tracking database."
    )
)
def disable_player_tracking(
    player_name: Annotated[str, Field(description="Name of the RuneScape player.")]
) -> dict[str, str]:

    """Disables tracking for a tracked player.
    Note that this does NOT REMOVE them from the database, so we can keep the original ids in place.
    Return ths username if updates successfully."""

    with get_db_session(db_url=config.DB_URL) as db:
        tracked_user: ProdTrackedUsers = (
            db.query(ProdTrackedUsers)
            .filter(
                ProdTrackedUsers.player_name == player_name,
                ProdTrackedUsers.is_active.is_(True))
            .one_or_none()
        )
        if not tracked_user:
            raise NotFoundError(f"No tracking active for '{player_name}'")
        tracked_user.is_active = False
        db.commit()
        return {
            "disabled_tracking": tracked_user.player_name
        }