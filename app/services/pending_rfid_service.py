"""
PendingRFID Service
Business Logic Layer für PendingRFID-Operationen.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from ..repositories import PendingRFIDRepository, EntityRepository
from ..schemas.pending_rfid import PendingRFIDCreate
from ..schemas.entity import EntityCreate
from ..models.pending_rfid import PendingRFID
from ..models.entity import Entity


class PendingRFIDService:
    """Service für PendingRFID-Business-Logic."""

    def __init__(self):
        self.repository = PendingRFIDRepository()
        self.entity_repository = EntityRepository()

    def get_all(self, db: Session, limit: int = 50) -> List[PendingRFID]:
        """Gibt alle PendingRFIDs zurück (neueste zuerst)."""
        return self.repository.get_recent(db, limit)

    def get_by_id(self, db: Session, pending_id: int) -> Optional[PendingRFID]:
        """Gibt einen PendingRFID anhand der ID zurück."""
        return self.repository.get_by_id(db, pending_id)

    def get_by_rfid(self, db: Session, rfid_id: str) -> Optional[PendingRFID]:
        """Gibt einen PendingRFID anhand der RFID-Nummer zurück."""
        return self.repository.get_by_rfid(db, rfid_id)

    def register_unknown_rfid(self, db: Session, rfid_id: str) -> PendingRFID:
        """
        Registriert einen unbekannten RFID-Tag.
        Wenn bereits vorhanden, erhöht den Counter.

        Args:
            db: Datenbank-Session
            rfid_id: RFID-Tag-Nummer

        Returns:
            PendingRFID (neu oder aktualisiert)
        """
        # Prüfe ob bereits vorhanden
        existing = self.repository.get_by_rfid(db, rfid_id)

        if existing:
            # Erhöhe Counter
            return self.repository.increment_scan_count(db, rfid_id)
        else:
            # Erstelle neuen Eintrag
            pending_data = PendingRFIDCreate(rfid_id=rfid_id)
            return self.repository.create(db, pending_data.model_dump())

    def convert_to_entity(
        self,
        db: Session,
        pending_id: int,
        entity_data: EntityCreate
    ) -> Optional[Entity]:
        """
        Konvertiert einen PendingRFID zu einer vollständigen Entity.
        Löscht den PendingRFID nach erfolgreicher Konvertierung.

        Args:
            db: Datenbank-Session
            pending_id: PendingRFID-ID
            entity_data: Entity-Daten (muss rfid_id vom PendingRFID enthalten)

        Returns:
            Neu erstellte Entity oder None bei Fehler

        Raises:
            ValueError: Wenn RFID-IDs nicht übereinstimmen oder RFID bereits als Entity existiert
        """
        # Hole PendingRFID
        pending = self.repository.get_by_id(db, pending_id)
        if not pending:
            return None

        # Prüfe ob RFID-IDs übereinstimmen
        if entity_data.rfid_id != pending.rfid_id:
            raise ValueError(
                f"RFID-ID mismatch: Entity hat '{entity_data.rfid_id}', "
                f"Pending hat '{pending.rfid_id}'"
            )

        # Prüfe ob RFID bereits als Entity existiert
        if self.entity_repository.exists_rfid(db, entity_data.rfid_id):
            raise ValueError(f"RFID-ID '{entity_data.rfid_id}' ist bereits als Entity registriert")

        # Erstelle Entity
        entity = self.entity_repository.create(db, entity_data.model_dump())

        # Lösche PendingRFID
        self.repository.delete(db, pending_id)

        return entity

    def delete(self, db: Session, pending_id: int) -> Optional[PendingRFID]:
        """
        Löscht einen PendingRFID.

        Args:
            db: Datenbank-Session
            pending_id: PendingRFID-ID

        Returns:
            Gelöschter PendingRFID oder None
        """
        return self.repository.delete(db, pending_id)

