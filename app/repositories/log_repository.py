"""
Log Repository
Data Access Layer für AccessLog-Operationen.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from .base import BaseRepository
from ..models.access_log import AccessLog


class LogRepository(BaseRepository[AccessLog]):
    """Repository für AccessLog-Datenbankoperationen."""

    def __init__(self):
        super().__init__(AccessLog)

    def get_by_entity(self, db: Session, entity_id: int, limit: int = 100) -> List[AccessLog]:
        """
        Gibt alle Logs einer Entity zurück.

        Args:
            db: Datenbank-Session
            entity_id: Entity-ID
            limit: Maximale Anzahl Einträge

        Returns:
            Liste von AccessLog-Einträgen
        """
        return (db.query(AccessLog)
                .filter(AccessLog.entity_id == entity_id)
                .order_by(AccessLog.timestamp.desc())
                .limit(limit)
                .all())

    def get_by_action(self, db: Session, action: str, limit: int = 100) -> List[AccessLog]:
        """
        Gibt alle Logs mit einer bestimmten Aktion zurück.

        Args:
            db: Datenbank-Session
            action: Aktionstyp (z.B. 'granted', 'unknown')
            limit: Maximale Anzahl Einträge

        Returns:
            Liste von AccessLog-Einträgen
        """
        return (db.query(AccessLog)
                .filter(AccessLog.action == action)
                .order_by(AccessLog.timestamp.desc())
                .limit(limit)
                .all())

    def get_recent(self, db: Session, limit: int = 100) -> List[AccessLog]:
        """
        Gibt die neuesten Logs zurück.

        Args:
            db: Datenbank-Session
            limit: Maximale Anzahl Einträge

        Returns:
            Liste von AccessLog-Einträgen
        """
        return (db.query(AccessLog)
                .order_by(AccessLog.timestamp.desc())
                .limit(limit)
                .all())

    def get_by_date_range(
        self,
        db: Session,
        start_date: datetime,
        end_date: datetime
    ) -> List[AccessLog]:
        """
        Gibt Logs in einem Datumsbereich zurück.

        Args:
            db: Datenbank-Session
            start_date: Start-Datum
            end_date: End-Datum

        Returns:
            Liste von AccessLog-Einträgen
        """
        return (db.query(AccessLog)
                .filter(AccessLog.timestamp >= start_date)
                .filter(AccessLog.timestamp <= end_date)
                .order_by(AccessLog.timestamp.desc())
                .all())

