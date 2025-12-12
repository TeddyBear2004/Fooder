"""
SystemSettings Database Model
Globale System-Einstellungen für Fooder.
"""
from sqlalchemy import Column, Integer, String, JSON
from ..database import Base


class SystemSettings(Base):
    """
    SystemSettings Model - Globale System-Einstellungen.

    Singleton-Tabelle (sollte nur einen Eintrag haben).

    Attributes:
        id: Eindeutige ID (immer 1)
        pending_door_values: JSON mit Standard-Türwerten für unbekannte RFIDs
                            Beispiel: {"door_1": 2.0, "door_2": 0.0}
        settings_json: JSON mit weiteren Einstellungen (für zukünftige Features)
    """
    __tablename__ = 'system_settings'

    id = Column(Integer, primary_key=True, default=1)
    pending_door_values = Column(JSON, nullable=False, default=dict)
    settings_json = Column(JSON, nullable=True, default=dict)

    def __repr__(self):
        return f"<SystemSettings(id={self.id}, pending_door_values={self.pending_door_values})>"

