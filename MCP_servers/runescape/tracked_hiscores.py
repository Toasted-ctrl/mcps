from sqlalchemy import Column, Integer, String, func, DateTime, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase

from config import mcp_config
from db import get_db_session

class Base(DeclarativeBase):
    pass

class StageTrackedUsersHiscores_1(Base):
    __tablename__ = 'stg_tracked_users_hs_1'

    source_id = Column(Integer)
    username = Column(String(50), primary_key=True)

class ProdMCPTrackedUsers(Base):
    __tablename__ = 'prod_mcp_tracked_users'
    
    username = Column(String(50), primary_key=True)
    inserted = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    inserted_by = Column(String(50), server_default=text("current_user"))

def get_tracked_hs_users() -> list:
    with get_db_session(db_url=mcp_config.db_url) as db:
        db.flush()
        result = db.query(StageTrackedUsersHiscores_1.username).all()
        return [row.username for row in result]
    
def post_tracked_user(username: str) -> str:

    """Processes new user to be tracked. Returns the username if added successfully."""

    with get_db_session(db_url=mcp_config.db_url) as db:
        if not (
            db.query(StageTrackedUsersHiscores_1.username)
            .filter(StageTrackedUsersHiscores_1.username == username)
            .scalar()
        ):
            try:
                db.add(ProdMCPTrackedUsers(username=username))
                db.commit()
            except IntegrityError as e:
                db.rollback()
                if e.orig.pgcode == '23505': # unique_violation
                    return username
                raise
        return username