"""
PendingRFID Pydantic Schemas
Schemas für API-Validierung und Serialisierung.
"""
from datetime import datetime
from pydantic import BaseModel, Field


class PendingRFIDBase(BaseModel):
    """Base Schema für PendingRFID."""
    rfid_id: str = Field(..., max_length=64, description="RFID-Tag-Nummer")


class PendingRFIDCreate(PendingRFIDBase):
    """Schema für PendingRFID-Erstellung."""
    pass


class PendingRFID(PendingRFIDBase):
    """Schema für PendingRFID-Antworten."""
    id: int
    first_seen: datetime
    last_seen: datetime
    scan_count: int

    class Config:
        from_attributes = True

