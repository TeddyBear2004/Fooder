"""
Entity Service
Business Logic Layer für Entity-Operationen.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from ..repositories import EntityRepository, LogRepository
from ..schemas.entity import EntityCreate
from ..models.entity import Entity


class EntityService:
    """Service für Entity-Business-Logic."""

    def __init__(self):
        self.repository = EntityRepository()
        self.log_repository = LogRepository()

    def get_all(self, db: Session) -> List[Entity]:
        """Gibt alle Entities zurück."""
        return self.repository.get_all(db)

    def get_by_id(self, db: Session, entity_id: int) -> Optional[Entity]:
        """Gibt eine Entity anhand der ID zurück."""
        return self.repository.get_by_id(db, entity_id)

    def get_by_rfid(self, db: Session, rfid_id: str) -> Optional[Entity]:
        """Gibt eine Entity anhand der RFID-ID zurück."""
        return self.repository.get_by_rfid(db, rfid_id)

    def create(self, db: Session, entity_data: EntityCreate) -> Entity:
        """
        Erstellt eine neue Entity.

        Args:
            db: Datenbank-Session
            entity_data: Entity-Daten

        Returns:
            Erstellte Entity

        Raises:
            ValueError: Wenn RFID-ID bereits existiert
        """
        # Prüfe, ob RFID bereits existiert
        if self.repository.exists_rfid(db, entity_data.rfid_id):
            raise ValueError(f"RFID-ID '{entity_data.rfid_id}' existiert bereits")

        return self.repository.create(db, entity_data.model_dump())

    def update(self, db: Session, entity_id: int, entity_data: EntityCreate) -> Optional[Entity]:
        """
        Aktualisiert eine Entity.

        Args:
            db: Datenbank-Session
            entity_id: Entity-ID
            entity_data: Neue Entity-Daten

        Returns:
            Aktualisierte Entity oder None
        """
        # Prüfe, ob Entity existiert
        existing = self.repository.get_by_id(db, entity_id)
        if not existing:
            return None

        # Prüfe, ob neue RFID-ID bereits von anderer Entity verwendet wird
        if entity_data.rfid_id != existing.rfid_id:
            if self.repository.exists_rfid(db, entity_data.rfid_id):
                raise ValueError(f"RFID-ID '{entity_data.rfid_id}' wird bereits verwendet")

        return self.repository.update(db, entity_id, entity_data.model_dump())

    def delete(self, db: Session, entity_id: int) -> Optional[Entity]:
        """
        Löscht eine Entity.

        Args:
            db: Datenbank-Session
            entity_id: Entity-ID

        Returns:
            Gelöschte Entity oder None
        """
        return self.repository.delete(db, entity_id)

