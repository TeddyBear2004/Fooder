"""
DoorSetting Pydantic Schemas
Schemas für API-Validierung und Serialisierung.
"""
from pydantic import BaseModel, Field


class DoorSettingBase(BaseModel):
    """Base Schema für DoorSetting mit gemeinsamen Feldern."""
    door_name: str = Field(..., max_length=50, description="Name der Tür (z.B. 'door_1')")
    servo_pin: int = Field(..., description="GPIO-Pin-Nummer des Servos")
    min_angle: float = Field(..., description="Minimaler Servo-Winkel in Grad")
    max_angle: float = Field(..., description="Maximaler Servo-Winkel in Grad")
    min_pulse: float = Field(0.0005, description="Minimale PWM-Pulsbreite in Sekunden")
    max_pulse: float = Field(0.0025, description="Maximale PWM-Pulsbreite in Sekunden")


class DoorSettingCreate(DoorSettingBase):
    """Schema für DoorSetting-Erstellung."""
    pass


class DoorSetting(DoorSettingBase):
    """Schema für DoorSetting-Antworten (inkl. ID)."""
    id: int

    class Config:
        from_attributes = True

