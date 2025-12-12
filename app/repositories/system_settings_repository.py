"""
SystemSettings Repository
Data Access Layer für SystemSettings-Operationen.
"""
from typing import Optional
from sqlalchemy.orm import Session
from ..models.system_settings import SystemSettings


class SystemSettingsRepository:
    """Repository für SystemSettings-Datenbankoperationen."""

    SINGLETON_ID = 1

    def get(self, db: Session) -> Optional[SystemSettings]:
        """
        Gibt die SystemSettings zurück (Singleton).

        Args:
            db: Datenbank-Session

        Returns:
            SystemSettings oder None
        """
        return db.query(SystemSettings).filter(SystemSettings.id == self.SINGLETON_ID).first()

    def get_or_create(self, db: Session) -> SystemSettings:
        """
        Gibt die SystemSettings zurück oder erstellt sie mit Defaults.

        Args:
            db: Datenbank-Session

        Returns:
            SystemSettings
        """
        settings = self.get(db)
        if not settings:
            settings = SystemSettings(
                id=self.SINGLETON_ID,
                pending_door_values={},
                settings_json={}
            )
            db.add(settings)
            db.commit()
            db.refresh(settings)
        return settings

    def update(self, db: Session, update_data: dict) -> SystemSettings:
        """
        Aktualisiert die SystemSettings.

        Args:
            db: Datenbank-Session
            update_data: Update-Daten

        Returns:
            Aktualisierte SystemSettings
        """
        settings = self.get_or_create(db)

        for key, value in update_data.items():
            if value is not None:  # Nur nicht-None Werte updaten
                setattr(settings, key, value)

        db.commit()
        db.refresh(settings)
        return settings

