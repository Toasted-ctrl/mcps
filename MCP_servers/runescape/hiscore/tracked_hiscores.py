import uuid

from datetime import datetime, timedelta

from core.config import mcp_config
from db.errors import NotFoundError
from db.session import get_db_session
from db.schemas import ProdTrackedUsers, StageHiscores_1

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
    
def get_user_historical_hs_item(
    player_name: str,
    skill_or_activity: str = "Overall",
    date: str = None,
    time: str = None
) -> dict:
    
    if date is None:
        request_date = datetime(1970, 1, 1)

    elif date is not None:
        date_split = date.split('-')
        year = int(date_split[0])
        month = int(date_split[1])
        day = int(date_split[2])
        request_date = datetime(year, month, day)

    if time is not None:
        time_split = time.split(':')
        hours = int(time_split[0])
        minutes = int(time_split[1])
        request_date = request_date + timedelta(hours=hours, minutes=minutes)
    
    username = player_name.strip().replace(" ", "_")
    
    with get_db_session(db_url=mcp_config.db_url) as db:
        player_id: uuid.UUID = (
            db.query(ProdTrackedUsers.id)
            .filter(ProdTrackedUsers.player_name == username)
            .scalar()
        )
        if player_id is None:
            raise NotFoundError(f"No player found with name '{player_name}'")
        query = (
            db.query(
                StageHiscores_1.name,
                StageHiscores_1.ingest_date,
                StageHiscores_1.rank,
                StageHiscores_1.level,
                StageHiscores_1.type,
                StageHiscores_1.points)
            .filter(
                StageHiscores_1.source_id == player_id,
                StageHiscores_1.name == skill_or_activity,
                StageHiscores_1.ingest_date >= request_date
            )
            .order_by(
                StageHiscores_1.ingest_date.asc()
            )
            .first()
        )
        if query is None:
            raise NotFoundError(f"No historical records found for '{player_name}' from {request_date}")
        return query._asdict()