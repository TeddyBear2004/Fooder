"""
Servo Controller Module
Steuerung von Servomotoren über GPIO.
"""
import logging

try:
    from gpiozero import AngularServo
except ImportError:
    AngularServo = None

from .gpio_factory import get_gpio_factory

LOGGER = logging.getLogger(__name__)


class ServoController:
    """
    Controller für einen Servomotor.
    Korrigierte Version: Trennt physische Limits von logischen Zielwinkeln.
    """

    def __init__(
        self,
        pin: int,
        min_angle: float,  # Logischer Zielwinkel 1 (z.B. 0.0)
        max_angle: float,  # Logischer Zielwinkel 2 (z.B. 5.0)
        min_pulse: float,
        max_pulse: float
    ):
        if AngularServo is None:
            raise RuntimeError("gpiozero ist nicht installiert")

        self.pin = pin

        # Wir speichern Ihre gewünschten Zielwinkel separat
        self.target_min = min_angle
        self.target_max = max_angle

        factory = get_gpio_factory()

        try:
            # FIX: Wir initialisieren den Servo IMMER mit seinem vollen physischen Bereich (-90 bis 90).
            # Damit bleibt die Skalierung korrekt (1 Grad ist wirklich 1 Grad).
            # initial_value=None verhindert, dass der Servo beim Start automatisch auf 0° springt
            self.servo = AngularServo(
                pin,
                min_angle=-90,
                max_angle=90,
                min_pulse_width=min_pulse,
                max_pulse_width=max_pulse,
                initial_angle=max_pulse,
                pin_factory=factory
            )

            LOGGER.info(
                f"Servo auf Pin {pin} initialisiert. "
                f"Physisch: -90°..90°. Logische Ziele: {self.target_min}° und {self.target_max}°"
            )
        except Exception as e:
            LOGGER.error(f"Fehler beim Initialisieren des Servos auf Pin {pin}: {e}")
            raise

    def move_to_min(self) -> None:
        """
        Bewegt den Servo zur konfigurierten 'min_angle' Position.
        """
        try:
            LOGGER.debug(f"Bewege Servo Pin {self.pin} zu Ziel {self.target_min}°")
            # WICHTIG: Wir nutzen .angle statt .min()
            self.servo.angle = self.target_min
        except Exception as e:
            LOGGER.error(f"Fehler beim Bewegen des Servos auf Pin {self.pin}: {e}")
            raise

    def move_to_max(self) -> None:
        """
        Bewegt den Servo zur konfigurierten 'max_angle' Position.
        """
        try:
            LOGGER.debug(f"Bewege Servo Pin {self.pin} zu Ziel {self.target_max}°")
            # WICHTIG: Wir nutzen .angle statt .max()
            self.servo.angle = self.target_max
        except Exception as e:
            LOGGER.error(f"Fehler beim Bewegen des Servos auf Pin {self.pin}: {e}")
            raise

    def move_to_angle(self, angle: float) -> None:
        """
        Bewegt den Servo zu einem spezifischen Winkel.
        """
        try:
            # Sicherheitscheck für Hardware-Limits
            if not (-90 <= angle <= 90):
                LOGGER.warning(f"Winkel {angle}° liegt außerhalb des physischen Bereichs (-90 bis 90)")

            LOGGER.debug(f"Bewege Servo auf Pin {self.pin} zu {angle}°")
            self.servo.angle = angle
        except Exception as e:
            LOGGER.error(f"Fehler beim Bewegen des Servos auf Pin {self.pin} zu {angle}°: {e}")
            raise

    def close(self) -> None:
        """
        Schließt den Servo und gibt die Ressourcen frei.
        """
        try:
            if hasattr(self, 'servo') and self.servo:
                self.servo.close()
                LOGGER.debug(f"Servo auf Pin {self.pin} geschlossen")
        except Exception as e:
            LOGGER.warning(f"Fehler beim Schließen des Servos auf Pin {self.pin}: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __repr__(self):
        return (
            f"<ServoController(pin={self.pin}, "
            f"targets={self.target_min}° / {self.target_max}°)>"
        )