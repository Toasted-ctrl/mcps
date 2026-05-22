from sqlalchemy.exc import SQLAlchemyError

from core.config import mcp_config
from db.errors import NotFoundError
from db.session import get_db_session
from db.schemas import ProdTrackedUsers

def get_tracked_hs_users() -> list:
    with get_db_session(db_url=mcp_config.db_url) as db:
        query = (
            db.query(ProdTrackedUsers.player_name)
            .filter(ProdTrackedUsers.is_active.is_(True))
            .all()
        )
        if not query:
            return []
        return [row.player_name for row in query]
    
def post_tracked_user(player_name: str) -> str:

    """Processes new user to be tracked. Returns the username if added successfully."""

    with get_db_session(db_url=mcp_config.db_url) as db:
        tracked_player: ProdTrackedUsers = (
            db.query(ProdTrackedUsers)
            .filter(ProdTrackedUsers.player_name == player_name)
            .scalar()
        )
        if not tracked_player:
            new_tracked_player = ProdTrackedUsers(
                is_active=True,
                player_name=player_name
            )
            db.add(new_tracked_player)
            db.commit()
            return new_tracked_player.player_name
        if not tracked_player.is_active:
            tracked_player.is_active = True
            db.commit()
            return tracked_player.player_name
        raise ValueError(f"'{player_name}' is already tracked")

def disable_tracking(player_name: str) -> str:

    """Disables tracking for a tracked player.
    Note that this does NOT REMOVE them from the database, so we can keep the original ids in place.
    Return ths username if updates successfully."""

    with get_db_session(db_url=mcp_config.db_url) as db:
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
        return tracked_user.player_name