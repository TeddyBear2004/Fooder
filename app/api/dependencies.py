"""
API Dependencies Module
Enthält gemeinsame Abhängigkeiten für alle API-Endpunkte.
"""
from typing import Generator
from sqlalchemy.orm import Session
from app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependency für Datenbankzugriff.
    Erstellt eine neue Session für jeden Request und schließt sie danach.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

