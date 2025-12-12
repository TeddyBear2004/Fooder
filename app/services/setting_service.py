"""
Setting Service
Business Logic Layer für DoorSetting-Operationen.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from ..repositories import SettingRepository
from ..schemas.door_setting import DoorSettingCreate
from ..models.door_setting import DoorSetting


class SettingService:
    """Service für DoorSetting-Business-Logic."""

    def __init__(self):
        self.repository = SettingRepository()

    def get_all(self, db: Session) -> List[DoorSetting]:
        """Gibt alle Settings zurück."""
        return self.repository.get_all(db)

    def get_by_id(self, db: Session, setting_id: int) -> Optional[DoorSetting]:
        """Gibt ein Setting anhand der ID zurück."""
        return self.repository.get_by_id(db, setting_id)

    def get_by_door_name(self, db: Session, door_name: str) -> Optional[DoorSetting]:
        """Gibt ein Setting anhand des Tür-Namens zurück."""
        return self.repository.get_by_door_name(db, door_name)

    def create(self, db: Session, setting_data: DoorSettingCreate) -> DoorSetting:
        """
        Erstellt ein neues Setting.

        Args:
            db: Datenbank-Session
            setting_data: Setting-Daten

        Returns:
            Erstelltes Setting

        Raises:
            ValueError: Wenn Tür-Name bereits existiert
        """
        # Prüfe, ob door_name bereits existiert
        if self.repository.exists_door_name(db, setting_data.door_name):
            raise ValueError(f"Tür '{setting_data.door_name}' existiert bereits")

        # Validiere Winkel
        if setting_data.min_angle >= setting_data.max_angle:
            raise ValueError("min_angle muss kleiner als max_angle sein")

        # Validiere Pulse-Breiten
        if setting_data.min_pulse >= setting_data.max_pulse:
            raise ValueError("min_pulse muss kleiner als max_pulse sein")

        return self.repository.create(db, setting_data.model_dump())

    def update(self, db: Session, setting_id: int, setting_data: DoorSettingCreate) -> Optional[DoorSetting]:
        """
        Aktualisiert ein Setting.

        Args:
            db: Datenbank-Session
            setting_id: Setting-ID
            setting_data: Neue Setting-Daten

        Returns:
            Aktualisiertes Setting oder None
        """
        # Prüfe, ob Setting existiert
        existing = self.repository.get_by_id(db, setting_id)
        if not existing:
            return None

        # Prüfe, ob neuer door_name bereits von anderem Setting verwendet wird
        if setting_data.door_name != existing.door_name:
            if self.repository.exists_door_name(db, setting_data.door_name):
                raise ValueError(f"Tür '{setting_data.door_name}' wird bereits verwendet")

        # Winkel-Validierung: Beide Richtungen erlaubt
        # min_angle < max_angle: Normale Drehrichtung
        # min_angle > max_angle: Umgekehrte Drehrichtung
        # Keine Validierung nötig

        # Validiere Pulse-Breiten
        if setting_data.min_pulse >= setting_data.max_pulse:
            raise ValueError("min_pulse muss kleiner als max_pulse sein")

        return self.repository.update(db, setting_id, setting_data.model_dump())

    def delete(self, db: Session, setting_id: int) -> Optional[DoorSetting]:
        """
        Löscht ein Setting.

        Args:
            db: Datenbank-Session
            setting_id: Setting-ID

        Returns:
            Gelöschtes Setting oder None
        """
        return self.repository.delete(db, setting_id)

