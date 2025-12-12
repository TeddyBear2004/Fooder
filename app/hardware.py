import logging
from typing import Optional

from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from mfrc522 import MFRC522

LOGGER = logging.getLogger(__name__)

# Gemeinsame Factory-Instanz für alle Servos
_gpio_factory = None


def get_gpio_factory():
    """Gibt eine gemeinsame PiGPIOFactory-Instanz zurück."""
    global _gpio_factory
    if _gpio_factory is None:
        _gpio_factory = PiGPIOFactory()
    return _gpio_factory


class ServoController:
    def __init__(self, pin: int, min_angle: float, max_angle: float, min_pulse: float, max_pulse: float):
        self.pin = pin
        self.min_angle = min_angle
        self.max_angle = max_angle
        factory = get_gpio_factory()

        try:
            self.servo = AngularServo(pin,
                                      min_angle=min_angle,
                                      max_angle=max_angle,
                                      min_pulse_width=min_pulse,
                                      max_pulse_width=max_pulse,
                                      pin_factory=factory)
            LOGGER.info(f"Servo initialized on pin {pin} (range: {min_angle}° to {max_angle}°)")
        except Exception as e:
            LOGGER.error(f"Failed to initialize servo on pin {pin}: {e}")
            raise

    def move_to_min(self):
        try:
            LOGGER.debug(f"Moving servo on pin {self.pin} to min angle ({self.min_angle}°)")
            self.servo.min()
        except Exception as e:
            LOGGER.error(f"Error moving servo on pin {self.pin} to min: {e}")
            raise

    def move_to_max(self):
        try:
            LOGGER.debug(f"Moving servo on pin {self.pin} to max angle ({self.max_angle}°)")
            self.servo.max()
        except Exception as e:
            LOGGER.error(f"Error moving servo on pin {self.pin} to max: {e}")
            raise

    def close(self):
        """Schließt den Servo und gibt die Ressourcen frei."""
        try:
            if hasattr(self, 'servo') and self.servo:
                self.servo.close()
                LOGGER.debug(f"Servo on pin {self.pin} closed")
        except Exception as e:
            LOGGER.warning(f"Error closing servo on pin {self.pin}: {e}")


class RFIDReader:
    def __init__(self, spi_device: int = 0, speed: int = 50000):
        self.reader = MFRC522(device=spi_device, spd=speed)

    def read_once(self) -> Optional[int]:
        (status, _tag_type) = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
        if status != self.reader.MI_OK:
            return None
        (status, uid) = self.reader.MFRC522_Anticoll()
        if status != self.reader.MI_OK:
            return None
        rfid_id = 0
        for i in range(0, 4):
            rfid_id = (rfid_id << 8) + uid[i]
        LOGGER.info("RFID tag detected: %s", rfid_id)
        return rfid_id

