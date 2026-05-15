from sqlalchemy import Column, Integer, String, func, DateTime, text
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
    
def post_tracked_users(usernames: tuple):

    """Processes new users to be tracked. Returns a tuple with: list of newly added users,
    and list of users that were already tracked."""

    users = [arg for arg in usernames]
    new_users = []
    present_users = []
    with get_db_session(db_url=mcp_config.db_url) as db:
        for user in users:
            try:
                if not db.query(StageTrackedUsersHiscores_1.username == user).scalar():
                    db.add(ProdMCPTrackedUsers(username=user))
                    new_users.append(user)
                    continue
                present_users.append(user)
            except Exception:
                present_users.append(user)
        db.commit()
        return new_users, present_users