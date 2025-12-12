from pathlib import Path
from pydantic import BaseModel


class Settings(BaseModel):
    database_url: str = f"sqlite:///{Path(__file__).resolve().parent.parent / 'fooder.db'}"


settings = Settings()

