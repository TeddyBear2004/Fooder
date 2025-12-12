"""
RFID Reader Module
Liest RFID-Tags über MFRC522-Reader.
"""
import logging
from typing import Optional

try:
    from mfrc522 import MFRC522
except ImportError:
    MFRC522 = None

LOGGER = logging.getLogger(__name__)


class RFIDReader:
    """
    Reader für RFID-Tags über MFRC522.

    Attributes:
        reader: MFRC522-Instanz
    """

    def __init__(self, spi_device: int = 0, speed: int = 50000):
        """
        Initialisiert den RFID-Reader.

        Args:
            spi_device: SPI-Device-Nummer (default: 0)
            speed: SPI-Geschwindigkeit in Hz (default: 50000)

        Raises:
            RuntimeError: Wenn mfrc522 nicht verfügbar ist
        """
        if MFRC522 is None:
            raise RuntimeError("mfrc522 ist nicht installiert")

        try:
            self.reader = MFRC522(device=spi_device, spd=speed)
            LOGGER.info(
                f"RFID-Reader initialisiert (SPI Device: {spi_device}, "
                f"Speed: {speed} Hz)"
            )
        except Exception as e:
            LOGGER.error(f"Fehler beim Initialisieren des RFID-Readers: {e}")
            raise

    def read_once(self) -> Optional[int]:
        """
        Versucht, ein RFID-Tag zu lesen (non-blocking).

        Returns:
            RFID-ID als Integer oder None wenn kein Tag erkannt wurde
        """
        try:
            # Request für Tag
            (status, _tag_type) = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
            if status != self.reader.MI_OK:
                return None

            # Anti-Collision
            (status, uid) = self.reader.MFRC522_Anticoll()
            if status != self.reader.MI_OK:
                return None

            # Konvertiere UID zu Integer
            rfid_id = 0
            for i in range(0, 4):
                rfid_id = (rfid_id << 8) + uid[i]

            LOGGER.info(f"RFID-Tag erkannt: {rfid_id}")
            return rfid_id

        except Exception as e:
            LOGGER.error(f"Fehler beim Lesen des RFID-Tags: {e}")
            return None

    def read_continuous(self, callback, interval: float = 0.2):
        """
        Liest kontinuierlich RFID-Tags und ruft Callback auf.

        Args:
            callback: Funktion die bei erkanntem Tag aufgerufen wird (rfid_id)
            interval: Wartezeit zwischen Scans in Sekunden
        """
        import time

        LOGGER.info("Starte kontinuierliches RFID-Lesen...")

        try:
            while True:
                rfid_id = self.read_once()
                if rfid_id is not None:
                    callback(rfid_id)
                time.sleep(interval)
        except KeyboardInterrupt:
            LOGGER.info("RFID-Lesen durch Benutzer gestoppt")
        except Exception as e:
            LOGGER.error(f"Fehler beim kontinuierlichen RFID-Lesen: {e}")
            raise

    def __repr__(self):
        return "<RFIDReader(MFRC522)>"

