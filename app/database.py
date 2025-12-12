import os
from pathlib import Path

from sqlalchemy.engine.url import make_url
from sqlalchemy import create_engine
from .config import settings
from sqlalchemy.orm import sessionmaker, declarative_base

db_url = settings.database_url
connect_args: dict[str, bool] = {}
if db_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False
    url = make_url(db_url)
    if url.database and url.database != ":memory:":
        sqlite_path = Path(url.database)
        if not sqlite_path.is_absolute():
            sqlite_path = (Path(__file__).resolve().parent / sqlite_path).resolve()
        sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        normalized = sqlite_path.as_posix()
        url = url.set(database=normalized)
    db_url = str(url)

engine = create_engine(db_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
