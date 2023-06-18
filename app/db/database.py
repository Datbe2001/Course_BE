from functools import lru_cache
from typing import Iterator

import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from app.core.setting import settings


@lru_cache()
def get_session_maker() -> sessionmaker:
    engine = sa.create_engine(settings.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session_local


def get_db() -> Iterator[Session]:
    session_local = get_session_maker()
    session = session_local()

    try:
        yield session
    except Exception as exc:
        session.rollback()
        raise exc
    finally:
        session.close()
