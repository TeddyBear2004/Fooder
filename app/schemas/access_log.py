"""
AccessLog Pydantic Schemas
Schemas für API-Validierung und Serialisierung.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AccessLogBase(BaseModel):
    """Base Schema für AccessLog mit gemeinsamen Feldern."""
    action: str = Field(..., max_length=50, description="Art des Zugriffs")


class AccessLogCreate(AccessLogBase):
    """Schema für AccessLog-Erstellung."""
    entity_id: Optional[int] = Field(None, description="Verknüpfte Entity-ID (null bei unbekanntem RFID)")
    rfid_id: Optional[str] = Field(None, max_length=64, description="RFID-Nummer (optional, wichtig bei unbekannten Tags)")


class AccessLog(AccessLogBase):
    """Schema für AccessLog-Antworten (inkl. ID und Timestamp)."""
    id: int
    entity_id: Optional[int]
    rfid_id: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True

