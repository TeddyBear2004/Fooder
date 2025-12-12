"""
PendingRFID Database Model
Temporäre RFID-Tags die noch nicht als Entity registriert sind.
"""
from sqlalchemy import Column, Integer, String, DateTime, func
from ..database import Base


class PendingRFID(Base):
    """
    PendingRFID Model - Temporäre/unbekannte RFID-Tags.

    Werden automatisch erstellt wenn ein unbekannter Tag gescannt wird.
    Können später zu vollständigen Entities konvertiert werden.

    Attributes:
        id: Eindeutige ID
        rfid_id: RFID-Tag-Nummer
        first_seen: Zeitpunkt des ersten Scans
        last_seen: Zeitpunkt des letzten Scans
        scan_count: Anzahl der Scans
    """
    __tablename__ = 'pending_rfids'

    id = Column(Integer, primary_key=True, index=True)
    rfid_id = Column(String(64), unique=True, nullable=False, index=True)
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    scan_count = Column(Integer, default=1, nullable=False)

    def __repr__(self):
        return f"<PendingRFID(id={self.id}, rfid_id='{self.rfid_id}', scan_count={self.scan_count})>"

