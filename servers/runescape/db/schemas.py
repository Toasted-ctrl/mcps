import uuid

from datetime import datetime
from sqlalchemy import String, func, DateTime, text, UUID, Boolean, Integer, BigInteger
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

class StageHiscores_1(Base):
    __tablename__ = "stg_hiscores_1"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    ingest_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        nullable=False
    )

    ingest_source_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        nullable=False
    )

    ingest_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False
    )

    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        nullable=False
    )

    type: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    inserted_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now()
    )

    inserted_by: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        server_default=text("current_user")
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    rank: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    level: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    points: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )