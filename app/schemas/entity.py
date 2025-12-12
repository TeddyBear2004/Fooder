"""
Entity Pydantic Schemas
Schemas für API-Validierung und Serialisierung.
"""
from typing import Dict
from pydantic import BaseModel, Field, field_validator


class EntityBase(BaseModel):
    """Base Schema für Entity mit gemeinsamen Feldern."""
    rfid_id: str = Field(..., max_length=64, description="RFID-Tag-Nummer")
    identifier: str = Field(..., max_length=255, description="Name/Bezeichnung des Haustiers")
    door_values: Dict[str, float] = Field(
        default_factory=dict,
        description="Türöffnungszeiten in Sekunden. Key=door_name, Value=Sekunden (z.B. {'door_1': 5.0, 'door_2': 0.0})"
    )

    @field_validator('door_values')
    @classmethod
    def validate_door_values(cls, v):
        """Validiert, dass alle Werte >= 0 sind."""
        for door_name, seconds in v.items():
            if seconds < 0:
                raise ValueError(f"Türwert für '{door_name}' muss >= 0 sein (ist: {seconds})")
        return v


class EntityCreate(EntityBase):
    """Schema für Entity-Erstellung."""
    pass


class Entity(EntityBase):
    """Schema für Entity-Antworten (inkl. ID)."""
    id: int

    class Config:
        from_attributes = True

