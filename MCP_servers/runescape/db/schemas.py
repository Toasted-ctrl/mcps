import uuid

from datetime import datetime
from sqlalchemy import String, func, DateTime, text, UUID, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

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