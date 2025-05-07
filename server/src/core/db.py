import typing as t
from sqlalchemy.dialects import sqlite
from sqlalchemy.engine import create_engine, Engine
from sqlalchemy.types import BigInteger
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from core.config import settings


engine: Engine = create_engine(settings.DATABASE_URI, echo=settings.SHOW_SQL)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=Session,
    bind=engine,
)


def get_db() -> t.Generator[Session, None, None]:
    session: Session = SessionLocal()

    try:
        yield session
    except Exception as err:
        session.rollback()
        raise err
    finally:
        session.close()


Long = BigInteger().with_variant(sqlite.INTEGER(), 'sqlite')


class BaseModel(DeclarativeBase):
    pass
