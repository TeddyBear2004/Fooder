"""
PendingRFID Repository
Data Access Layer für PendingRFID-Operationen.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from .base import BaseRepository
from ..models.pending_rfid import PendingRFID


class PendingRFIDRepository(BaseRepository[PendingRFID]):
    """Repository für PendingRFID-Datenbankoperationen."""

    def __init__(self):
        super().__init__(PendingRFID)

    def get_by_rfid(self, db: Session, rfid_id: str) -> Optional[PendingRFID]:
        """
        Findet einen PendingRFID anhand der RFID-ID.

        Args:
            db: Datenbank-Session
            rfid_id: RFID-Tag-Nummer

        Returns:
            PendingRFID oder None
        """
        return db.query(PendingRFID).filter(PendingRFID.rfid_id == rfid_id).first()

    def increment_scan_count(self, db: Session, rfid_id: str) -> Optional[PendingRFID]:
        """
        Erhöht den Scan-Counter für eine RFID.
        Aktualisiert auch last_seen.

        Args:
            db: Datenbank-Session
            rfid_id: RFID-Tag-Nummer

        Returns:
            Aktualisiertes PendingRFID oder None
        """
        pending = self.get_by_rfid(db, rfid_id)
        if pending:
            pending.scan_count += 1
            pending.last_seen = func.now()
            db.commit()
            db.refresh(pending)
        return pending

    def get_recent(self, db: Session, limit: int = 50) -> List[PendingRFID]:
        """
        Gibt die neuesten PendingRFIDs zurück (nach last_seen sortiert).

        Args:
            db: Datenbank-Session
            limit: Maximale Anzahl

        Returns:
            Liste von PendingRFID-Einträgen
        """
        return (db.query(PendingRFID)
                .order_by(PendingRFID.last_seen.desc())
                .limit(limit)
                .all())

