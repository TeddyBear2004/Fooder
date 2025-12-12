"""
Entity Database Model
Repräsentiert ein Haustier mit RFID-Tag und Türwerten.
"""
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from ..database import Base


class Entity(Base):
    """
    Entity Model - Haustier mit RFID-Identifikation.

    Attributes:
        id: Eindeutige ID
        rfid_id: RFID-Tag-Nummer (eindeutig)
        identifier: Name/Bezeichnung des Haustiers
        door_values: JSON-Objekt mit Türnamen als Keys und Sekunden als Values
                     Beispiel: {"door_1": 5.0, "door_2": 2.5}
        logs: Beziehung zu AccessLog-Einträgen
    """
    __tablename__ = 'entities'

    id = Column(Integer, primary_key=True, index=True)
    rfid_id = Column(String(64), unique=True, nullable=False, index=True)
    identifier = Column(String(255), nullable=False)
    door_values = Column(JSON, nullable=False, default=dict)

    # Relationships
    logs = relationship('AccessLog', back_populates='entity')

    def __repr__(self):
        return f"<Entity(id={self.id}, rfid_id='{self.rfid_id}', identifier='{self.identifier}')>"

