import logging
import signal
import sys
import threading
from time import sleep, time
from typing import Dict, Optional

import requests

# Importieren Sie hier Ihre KORRIGIERTE ServoController Klasse
from .hardware import RFIDReader, ServoController

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("pi_agent")

API_BASE = "http://localhost:8080"
CONFIG_RELOAD_INTERVAL = 10


def fetch_door_settings() -> Dict[str, dict]:
    """Lädt Türkonfigurationen von der API."""
    try:
        resp = requests.get(f"{API_BASE}/settings", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        settings_map = {}
        for item in data:
            settings_map[item["door_name"]] = item
        return settings_map
    except requests.RequestException as exc:
        LOGGER.error("Failed to fetch door settings: %s", exc)
        return {}


def fetch_entities() -> dict:
    try:
        resp = requests.get(f"{API_BASE}/entities", timeout=5)
        resp.raise_for_status()
        return {entity["rfid_id"]: entity for entity in resp.json()}
    except requests.RequestException as exc:
        LOGGER.error("Failed to fetch entities: %s", exc)
        return {}


def fetch_pending_door_values() -> Dict[str, float]:
    try:
        resp = requests.get(f"{API_BASE}/system-settings", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return data.get("pending_door_values", {})
    except requests.RequestException as exc:
        LOGGER.error("Failed to fetch pending door values: %s", exc)
        return {}


def log_access(entity_id: Optional[int], action: str, rfid_id: Optional[str] = None):
    try:
        payload = {"entity_id": entity_id, "action": action}
        if rfid_id:
            payload["rfid_id"] = rfid_id
        requests.post(f"{API_BASE}/logs", json=payload, timeout=5)
    except requests.RequestException as exc:
        LOGGER.warning("Failed to post access log: %s", exc)


def reload_servos_if_needed(current_settings: Dict[str, dict],
                            servos: Dict[str, ServoController]) -> tuple[Dict[str, dict], Dict[str, ServoController]]:
    new_settings = fetch_door_settings()
    if not new_settings:
        LOGGER.warning("Could not reload settings, keeping current configuration")
        return current_settings, servos

    if new_settings == current_settings:
        return current_settings, servos

    LOGGER.info("Servo configuration changed, reloading controllers")

    for door_name, servo in servos.items():
        try:
            servo.close()
        except Exception as exc:
            LOGGER.warning(f"Error closing servo for {door_name}: {exc}")

    sleep(0.5)

    new_servos = {}
    for door_name, cfg in new_settings.items():
        try:
            # WICHTIG: Sichere Defaults verwenden (0 statt -90/90)
            # Damit der Servo bei DB-Fehler nicht wild ausschlägt.
            min_angle = cfg.get("min_angle", 0)
            max_angle = cfg.get("max_angle", 0)

            new_servos[door_name] = ServoController(
                pin=cfg["servo_pin"],
                min_angle=min_angle,
                max_angle=max_angle,
                min_pulse=cfg.get("min_pulse", 0.0005),
                max_pulse=cfg.get("max_pulse", 0.0025)
            )
            # Initial schließen
            new_servos[door_name].move_to_max()
            LOGGER.info(f"Reloaded '{door_name}' (Pin {cfg['servo_pin']}): Open={min_angle}°, Closed={max_angle}°")
        except Exception as exc:
            LOGGER.error("Failed to initialize servo '%s': %s", door_name, exc)

    return new_settings, new_servos


def operate_door(servo: ServoController, door_name: str, seconds: float):
    """
    Logik:
    move_to_min() -> Öffnen (Zielwinkel: min_angle aus Config)
    move_to_max() -> Schließen (Zielwinkel: max_angle aus Config)
    """
    try:
        if seconds <= 0:
            LOGGER.info("%s: Skipping (value=%.2f seconds, no opening)", door_name, seconds)
            return

        LOGGER.info("Opening %s for %.2f seconds", door_name, seconds)
        # HIER WIRD GEÖFFNET
        servo.move_to_min()
        sleep(seconds)

        LOGGER.info("Closing %s", door_name)
        # HIER WIRD GESCHLOSSEN
        servo.move_to_max()
    except Exception as exc:
        LOGGER.error("Error operating door %s: %s", door_name, exc)


def main_loop():
    reader = RFIDReader()
    door_settings = fetch_door_settings()

    if not door_settings:
        LOGGER.warning("Could not load door settings from API. Retry in 3s...")
        sleep(3)
        main_loop()
        return

    servos = {}
    for door_name, cfg in door_settings.items():
        try:
            min_angle = cfg.get("min_angle", 0)
            max_angle = cfg.get("max_angle", 0)

            servos[door_name] = ServoController(
                pin=cfg["servo_pin"],
                min_angle=min_angle,
                max_angle=max_angle,
                min_pulse=cfg.get("min_pulse", 0.0005),
                max_pulse=cfg.get("max_pulse", 0.0025)
            )
            servos[door_name].move_to_max()
            LOGGER.info(f"Initialized '{door_name}' on pin {cfg['servo_pin']}. Open={min_angle}°, Closed={max_angle}°")
        except Exception as exc:
            LOGGER.error("Failed to initialize servo '%s': %s", door_name, exc)

    LOGGER.info("Fooder Pi agent ready. Scan RFID tags.")

    def handle_sigterm(_signal, _frame):
        LOGGER.info("Stopping agent...")
        for door_name, servo in servos.items():
            try:
                servo.close()
            except Exception:
                pass
        sys.exit(0)

    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.signal(signal.SIGINT, handle_sigterm)

    last_config_reload = time()

    while True:
        if time() - last_config_reload > CONFIG_RELOAD_INTERVAL:
            door_settings, servos = reload_servos_if_needed(door_settings, servos)
            last_config_reload = time()

        rfid_id = reader.read_once()
        if rfid_id is None:
            sleep(0.2)
            continue

        entities = fetch_entities()
        entity = entities.get(str(rfid_id))

        if entity:
            LOGGER.info("RFID %s recognized as entity ID %d", rfid_id, entity["id"])
            log_access(entity["id"], "granted", rfid_id=str(rfid_id))
            door_values = entity.get("door_values", {})
        else:
            LOGGER.warning("Unknown RFID %s", rfid_id)
            log_access(None, "unknown", rfid_id=str(rfid_id))
            try:
                requests.post(f"{API_BASE}/pending-rfids", json={"rfid_id": str(rfid_id)}, timeout=5)
            except requests.RequestException:
                pass

            door_values = fetch_pending_door_values()

        # Threads starten
        threads = []
        for door_name, seconds in door_values.items():
            servo = servos.get(door_name)
            if servo is None:
                continue

            thread = threading.Thread(
                target=operate_door,
                args=(servo, door_name, seconds),
                name=f"door_{door_name}"
            )
            thread.start()
            threads.append(thread)

        # Warten bis Bewegung fertig ist (Blocking!)
        # Das verhindert, dass während des Öffnens schon der nächste Chip gelesen wird.
        # Das ist gut für die Stabilität.
        for thread in threads:
            thread.join()


if __name__ == "__main__":
    main_loop()