"""
GPIO Factory Module
Verwaltet eine gemeinsame PiGPIOFactory-Instanz.
"""
import logging

try:
    from gpiozero.pins.pigpio import PiGPIOFactory
except ImportError:
    PiGPIOFactory = None

LOGGER = logging.getLogger(__name__)

# Gemeinsame Factory-Instanz für alle GPIO-Operationen
_gpio_factory = None


def get_gpio_factory():
    """
    Gibt eine gemeinsame PiGPIOFactory-Instanz zurück.

    Returns:
        PiGPIOFactory-Instanz

    Raises:
        RuntimeError: Wenn gpiozero nicht verfügbar ist
    """
    global _gpio_factory

    if PiGPIOFactory is None:
        raise RuntimeError("gpiozero ist nicht installiert")

    if _gpio_factory is None:
        try:
            _gpio_factory = PiGPIOFactory()
            LOGGER.info("GPIO Factory initialisiert")
        except Exception as e:
            LOGGER.error(f"Fehler beim Initialisieren der GPIO Factory: {e}")
            raise

    return _gpio_factory


def reset_gpio_factory():
    """
    Setzt die GPIO Factory zurück.
    Nützlich für Tests oder bei Hardware-Problemen.
    """
    global _gpio_factory

    if _gpio_factory is not None:
        try:
            _gpio_factory.close()
        except Exception as e:
            LOGGER.warning(f"Fehler beim Schließen der GPIO Factory: {e}")
        finally:
            _gpio_factory = None
            LOGGER.info("GPIO Factory zurückgesetzt")

