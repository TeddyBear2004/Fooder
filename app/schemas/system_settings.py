"""
SystemSettings Pydantic Schemas
Schemas für globale System-Einstellungen.
"""
from typing import Dict, Optional
from pydantic import BaseModel, Field, field_validator


class SystemSettingsBase(BaseModel):
    """Base Schema für SystemSettings."""
    pending_door_values: Dict[str, float] = Field(
        default_factory=dict,
        description="Standard-Türwerte für unbekannte RFIDs in Sekunden. Key=door_name, Value=Sekunden"
    )
    settings_json: Optional[Dict] = Field(
        default_factory=dict,
        description="Weitere System-Einstellungen (JSON)"
    )

    @field_validator('pending_door_values')
    @classmethod
    def validate_pending_door_values(cls, v):
        """Validiert, dass alle Werte >= 0 sind."""
        for door_name, seconds in v.items():
            if seconds < 0:
                raise ValueError(f"Türwert für '{door_name}' muss >= 0 sein (ist: {seconds})")
        return v


class SystemSettingsCreate(SystemSettingsBase):
    """Schema für SystemSettings-Erstellung."""
    pass


class SystemSettingsUpdate(BaseModel):
    """Schema für SystemSettings-Update (alle Felder optional)."""
    pending_door_values: Optional[Dict[str, float]] = None
    settings_json: Optional[Dict] = None


class SystemSettings(SystemSettingsBase):
    """Schema für SystemSettings-Antworten."""
    id: int

    class Config:
        from_attributes = True

