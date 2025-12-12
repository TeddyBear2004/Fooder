"""
Log Service
Business Logic Layer für AccessLog-Operationen.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..repositories import LogRepository
from ..schemas.access_log import AccessLogCreate
from ..models.access_log import AccessLog


class LogService:
    """Service für AccessLog-Business-Logic."""

    def __init__(self):
        self.repository = LogRepository()

    def get_all(self, db: Session, limit: int = 100) -> List[AccessLog]:
        """
        Gibt alle Logs zurück (neueste zuerst).

        Args:
            db: Datenbank-Session
            limit: Maximale Anzahl Einträge

        Returns:
            Liste von AccessLog-Einträgen
        """
        return self.repository.get_recent(db, limit)

    def get_by_id(self, db: Session, log_id: int) -> Optional[AccessLog]:
        """Gibt einen Log anhand der ID zurück."""
        return self.repository.get_by_id(db, log_id)

    def get_by_entity(self, db: Session, entity_id: int, limit: int = 100) -> List[AccessLog]:
        """Gibt alle Logs einer Entity zurück."""
        return self.repository.get_by_entity(db, entity_id, limit)

    def get_by_action(self, db: Session, action: str, limit: int = 100) -> List[AccessLog]:
        """Gibt alle Logs mit einer bestimmten Aktion zurück."""
        return self.repository.get_by_action(db, action, limit)

    def get_by_date_range(
        self,
        db: Session,
        start_date: datetime,
        end_date: datetime
    ) -> List[AccessLog]:
        """Gibt Logs in einem Datumsbereich zurück."""
        return self.repository.get_by_date_range(db, start_date, end_date)

    def create(self, db: Session, log_data: AccessLogCreate) -> AccessLog:
        """
        Erstellt einen neuen Log-Eintrag.

        Args:
            db: Datenbank-Session
            log_data: Log-Daten

        Returns:
            Erstellter Log-Eintrag
        """
        return self.repository.create(db, log_data.model_dump())

    def log_access(self, db: Session, entity_id: Optional[int], action: str) -> AccessLog:
        """
        Convenience-Methode zum Erstellen eines Access-Logs.

        Args:
            db: Datenbank-Session
            entity_id: Entity-ID (None bei unbekanntem RFID)
            action: Aktionstyp

        Returns:
            Erstellter Log-Eintrag
        """
        log_data = AccessLogCreate(entity_id=entity_id, action=action)
        return self.create(db, log_data)

