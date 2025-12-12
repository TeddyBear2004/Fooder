"""
DoorSetting Database Model
Repräsentiert die Hardware-Konfiguration für einen Servomotor.
"""
from sqlalchemy import Column, Integer, String, Float
from ..database import Base


class DoorSetting(Base):
    """
    DoorSetting Model - Servomotor-Konfiguration für eine Tür.

    Attributes:
        id: Eindeutige ID
        door_name: Name der Tür (z.B. 'door_1', 'door_2')
        servo_pin: GPIO-Pin-Nummer des Servos
        min_angle: Minimaler Servo-Winkel in Grad
        max_angle: Maximaler Servo-Winkel in Grad
        min_pulse: Minimale PWM-Pulsbreite in Sekunden
        max_pulse: Maximale PWM-Pulsbreite in Sekunden
    """
    __tablename__ = 'door_settings'

    id = Column(Integer, primary_key=True, index=True)
    door_name = Column(String(50), unique=True, nullable=False, index=True)
    servo_pin = Column(Integer, nullable=False)
    min_angle = Column(Float, nullable=False)
    max_angle = Column(Float, nullable=False)
    min_pulse = Column(Float, nullable=False, default=0.0005)
    max_pulse = Column(Float, nullable=False, default=0.0025)

    def __repr__(self):
        return f"<DoorSetting(id={self.id}, door_name='{self.door_name}', servo_pin={self.servo_pin})>"

