import uuid

from datetime import datetime
from sqlalchemy import String, func, DateTime, text, UUID, Boolean
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import mcp_config
from db import get_db_session

class Base(DeclarativeBase):
    pass

class ProdTrackedUsers(Base):
    __tablename__ = "prod_tracked_users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    
    player_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )
    
    inserted_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now()
    )
    
    inserted_by: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        server_default=text("current_user")
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

def get_tracked_hs_users() -> list:
    with get_db_session(db_url=mcp_config.db_url) as db:
        db.flush()
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

    # TODO: If a player already exists as name, create function to check if is_active is False.
    # TODO: If it is false, update to True.

    with get_db_session(db_url=mcp_config.db_url) as db:
        db.flush()
        try:
            db.add(ProdTrackedUsers(player_name=player_name, is_active=True))
            db.commit()
            return player_name
        except IntegrityError as e:
            db.rollback()
            if e.orig.pg_code == "23505": # NOTE: Unique violation code
                return player_name
            raise
