"""
Setting Repository
Data Access Layer für DoorSetting-Operationen.
"""
from typing import Optional
from sqlalchemy.orm import Session
from .base import BaseRepository
from ..models.door_setting import DoorSetting


class SettingRepository(BaseRepository[DoorSetting]):
    """Repository für DoorSetting-Datenbankoperationen."""

    def __init__(self):
        super().__init__(DoorSetting)

    def get_by_door_name(self, db: Session, door_name: str) -> Optional[DoorSetting]:
        """
        Findet ein Setting anhand des Tür-Namens.

        Args:
            db: Datenbank-Session
            door_name: Name der Tür (z.B. 'door_1')

        Returns:
            DoorSetting oder None
        """
        return db.query(DoorSetting).filter(DoorSetting.door_name == door_name).first()

    def exists_door_name(self, db: Session, door_name: str) -> bool:
        """
        Prüft, ob ein Tür-Name bereits existiert.

        Args:
            db: Datenbank-Session
            door_name: Name der Tür

        Returns:
            True wenn existiert, sonst False
        """
        return db.query(DoorSetting).filter(DoorSetting.door_name == door_name).count() > 0

