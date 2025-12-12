"""
SystemSettings Service
Business Logic Layer für SystemSettings-Operationen.
"""
from typing import Dict
from sqlalchemy.orm import Session
from ..repositories import SystemSettingsRepository
from ..schemas.system_settings import SystemSettingsUpdate
from ..models.system_settings import SystemSettings


class SystemSettingsService:
    """Service für SystemSettings-Business-Logic."""

    def __init__(self):
        self.repository = SystemSettingsRepository()

    def get(self, db: Session) -> SystemSettings:
        """
        Gibt die globalen SystemSettings zurück.
        Erstellt sie automatisch mit Defaults falls nicht vorhanden.
        """
        return self.repository.get_or_create(db)

    def update(self, db: Session, update_data: SystemSettingsUpdate) -> SystemSettings:
        """
        Aktualisiert die SystemSettings.

        Args:
            db: Datenbank-Session
            update_data: Update-Daten

        Returns:
            Aktualisierte SystemSettings
        """
        # Validiere pending_door_values falls vorhanden
        if update_data.pending_door_values is not None:
            for door_name, seconds in update_data.pending_door_values.items():
                if seconds < 0:
                    raise ValueError(f"Türwert für '{door_name}' muss >= 0 sein")

        return self.repository.update(db, update_data.model_dump(exclude_none=True))

    def get_pending_door_values(self, db: Session) -> Dict[str, float]:
        """
        Gibt die konfigurierten pending_door_values zurück.

        Returns:
            Dictionary mit door_name → Sekunden
        """
        settings = self.get(db)
        return settings.pending_door_values or {}

