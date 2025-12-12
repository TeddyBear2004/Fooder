"""
Entity Repository
Data Access Layer für Entity-Operationen.
"""
from typing import Optional
from sqlalchemy.orm import Session
from .base import BaseRepository
from ..models.entity import Entity


class EntityRepository(BaseRepository[Entity]):
    """Repository für Entity-Datenbankoperationen."""

    def __init__(self):
        super().__init__(Entity)

    def get_by_rfid(self, db: Session, rfid_id: str) -> Optional[Entity]:
        """
        Findet eine Entity anhand der RFID-ID.

        Args:
            db: Datenbank-Session
            rfid_id: RFID-Tag-Nummer

        Returns:
            Entity oder None
        """
        return db.query(Entity).filter(Entity.rfid_id == rfid_id).first()

    def exists_rfid(self, db: Session, rfid_id: str) -> bool:
        """
        Prüft, ob eine RFID-ID bereits existiert.

        Args:
            db: Datenbank-Session
            rfid_id: RFID-Tag-Nummer

        Returns:
            True wenn existiert, sonst False
        """
        return db.query(Entity).filter(Entity.rfid_id == rfid_id).count() > 0

