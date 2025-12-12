from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base

class Entity(Base):
    __tablename__ = 'entities'
    id = Column(Integer, primary_key=True, index=True)
    rfid_id = Column(String(64), unique=True, nullable=False)
    identifier = Column(String(255), nullable=False)
    door1_value = Column(Float, nullable=False, default=0.0)
    door2_value = Column(Float, nullable=False, default=0.0)
    logs = relationship('AccessLog', back_populates='entity')

class DoorSetting(Base):
    __tablename__ = 'door_settings'
    id = Column(Integer, primary_key=True, index=True)
    door_name = Column(String(50), unique=True, nullable=False)
    servo_pin = Column(Integer, nullable=False)
    min_angle = Column(Float, nullable=False)
    max_angle = Column(Float, nullable=False)
    min_pulse = Column(Float, nullable=False, default=0.0005)
    max_pulse = Column(Float, nullable=False, default=0.0025)

class AccessLog(Base):
    __tablename__ = 'access_logs'
    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer, ForeignKey('entities.id'), nullable=True)
    action = Column(String(50), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    entity = relationship('Entity', back_populates='logs')
