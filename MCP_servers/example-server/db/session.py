from collections.abc import Iterator
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

@contextmanager
def get_db_session(db_url: str) -> Iterator[Session]:
    engine = create_engine(url=db_url, echo=False)
    SessionLocal = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False
    )
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        engine.dispose()