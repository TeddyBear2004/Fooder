from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EntityBase(BaseModel):
    rfid_id: str = Field(..., max_length=64)
    identifier: str = Field(..., max_length=255)
    door1_value: float = Field(..., ge=0.0, le=1.0)
    door2_value: float = Field(..., ge=0.0, le=1.0)

class EntityCreate(EntityBase):
    pass

class Entity(EntityBase):
    id: int
    class Config:
        from_attributes = True  # Changed from orm_mode


class DoorSettingBase(BaseModel):
    door_name: str = Field(..., max_length=50)
    servo_pin: int
    min_angle: float
    max_angle: float
    min_pulse: float = 0.0005
    max_pulse: float = 0.0025

class DoorSettingCreate(DoorSettingBase):
    pass

class DoorSetting(DoorSettingBase):
    id: int
    class Config:
        from_attributes = True  # Changed from orm_mode


class AccessLogBase(BaseModel):
    action: str = Field(..., max_length=50)

class AccessLogCreate(AccessLogBase):
    entity_id: Optional[int]

class AccessLog(AccessLogBase):
    id: int
    entity_id: Optional[int]
    timestamp: datetime
    class Config:
        from_attributes = True  # Changed from orm_mode