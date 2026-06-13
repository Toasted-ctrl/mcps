from ...config import config
from ...db.schemas import ProdTrackedUsers
from ...server import mcp

from shared.db import get_db_session
from shared.errors import NotFoundError

@mcp.tool(
    name="get_players_tracked_hiscores",
    version="1.0.1",
    meta={
        "author": "Toasted-ctrl"
    },
    description=(
        "Retrieves a list of players / usernames for which currently historical hiscore data is being tracked. "
        "Only use this tool when the user is asking for information on who / what player / what user is being tracked when it regards hiscores. "
        "Returns: a list of tracked usernames."
    )
)
def get_players_tracked_hiscores() -> dict:
    with get_db_session(db_url=config.DB_URL) as db:
        query = (
            db.query(ProdTrackedUsers.player_name)
            .filter(ProdTrackedUsers.is_active.is_(True))
            .all()
        )
        if not query:
            raise NotFoundError("No tracked players in database")
        return {
            "tracked_players_hiscores": [row.player_name for row in query]
        }