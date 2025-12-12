"""
AccessLog Database Model
Protokolliert Zugriffe auf das System.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from ..database import Base


class AccessLog(Base):
    """
    AccessLog Model - Zugriffsprotokolle.

    Attributes:
        id: Eindeutige ID
        entity_id: Verknüpfung zur Entity (null bei unbekanntem RFID)
        action: Art des Zugriffs (granted, unknown, read, update, delete, etc.)
        rfid_id: RFID-Nummer (optional, besonders bei unbekannten Tags)
        timestamp: Zeitpunkt des Zugriffs
        entity: Beziehung zum Entity-Objekt
    """
    __tablename__ = 'access_logs'

    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer, ForeignKey('entities.id'), nullable=True, index=True)
    action = Column(String(50), nullable=False, index=True)
    rfid_id = Column(String(64), nullable=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    entity = relationship('Entity', back_populates='logs')

    def __repr__(self):
        return f"<AccessLog(id={self.id}, entity_id={self.entity_id}, rfid_id='{self.rfid_id}', action='{self.action}', timestamp={self.timestamp})>"

