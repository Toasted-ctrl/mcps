from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

from config import mcp_config
from db import get_db_session

class Base(DeclarativeBase):
    pass

class StageTrackedUsersHiscores_1(Base):
    __tablename__ = 'stg_tracked_users_hs_1'

    source_id = Column(Integer)
    username = Column(String(50), primary_key=True)

def get_tracked_hs_users():
    with get_db_session(db_url=mcp_config.db_url) as db:
        db.flush()
        result = db.query(StageTrackedUsersHiscores_1.username).all()
        return [row.username for row in result]