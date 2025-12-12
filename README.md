# Fooder API

FastAPI-gestützte REST-API zur Verwaltung von RFID-Entitäten, Tür-Servoeinstellungen und Zugriffslog.

> **🆕 Version 2.1 - Dynamic Doors & RFID Logging**  
> - ✅ Dynamische Türen-Anzahl (JSON-basiert)
> - ✅ Direkte Sekundenwerte (keine 0..1 Multiplikation)
> - ✅ RFID-Logging bei unbekannten Tags
> - ✅ Keine hardcodierten Default-Werte
> 
> Siehe `CHANGES_V2.1.md` für alle Änderungen.  
> Siehe `ARCHITECTURE.md` für Details zur Architektur.  
> Siehe `MIGRATION.md` für Migrations-Hinweise.

## Features
- CRUD-Endpunkte für Entitäten (RFID), Tür-Settings und Zugriff-Logs
- SQLite-Datenbank ohne Authentifizierung
- Pro Entität Werte zwischen 0 und 1 für zwei Türen
- Settings definieren Servo-Pins und Winkel
- Logging, welche Entität wann auf die API zugreift
- CORS-Unterstützung für alle Origins (ideal für Weboberflächen)

## Setup
1. Virtuelle Umgebung aktivieren (falls nicht aktiv)
2. Abhängigkeiten installieren:

```powershell
pip install -r requirements.txt
```

3. Server starten:

```powershell
uvicorn app.main:app --reload
```

## Nutzung
- `POST /entities` erzeugt eine neue Entität (RFID-ID, Identifier, Tür-Werte)
- `POST /settings` konfiguriert Servos für Türen
- Alle CRUD-Methoden für beide Ressourcen verfügbar
- Jeder Zugriff auf Entitäten erzeugt automatisch einen Logeintrag

## Raspberry Pi Deployment
1. Auf dem Pi `sudo apt update && sudo apt install pigpio python3-dev build-essential`
2. `pip install -r requirements.txt`
3. pigpiod-Server starten: `sudo systemctl enable pigpiod && sudo systemctl start pigpiod`
4. FastAPI-Server auf dem Pi oder separatem Rechner starten (`uvicorn app.main:app --host 0.0.0.0 --port 8000`)
5. API mit initialen Daten befüllen (`/settings` für jede Tür, `/entities` für RFID-Karten)
6. Pi-Agent starten: `python -m app.pi_agent`

### Hardware-Agent konfigurieren
- `app/pi_agent.py` liest zyklisch RFID-Tags, ruft `/entities` ab und steuert Servos gemäß den gespeicherten Werten
- Benötigt laufende API unter `API_BASE` (Default `http://localhost:8080`; bei Remote-Server IP/Port anpassen)
- Bei erfolgreicher Erkennung schreibt der Agent zusätzliche Logeinträge via `/logs`

## Troubleshooting

### "Could not load initial door settings"
Dieser Fehler tritt auf, wenn die Datenbank keine Türeinstellungen enthält. Es gibt zwei Lösungen:

**Lösung 1: Automatische Standard-Initialisierung (Empfohlen)**
```bash
python3 quick_init.py
```
Dies erstellt automatisch Standard-Einstellungen für door_1 (Pin 17) und door_2 (Pin 27).

**Lösung 2: Manuelle Initialisierung über die API**
Starte die API und füge Türeinstellungen hinzu:
```bash
# API starten
uvicorn app.main:app --host 0.0.0.0 --port 8080

# In einem anderen Terminal:
curl -X POST "http://localhost:8080/settings" \
  -H "Content-Type: application/json" \
  -d '{
    "door_name": "door_1",
    "servo_pin": 17,
    "min_angle": -90,
    "max_angle": 90,
    "min_pulse": 0.0005,
    "max_pulse": 0.0025
  }'

curl -X POST "http://localhost:8080/settings" \
  -H "Content-Type: application/json" \
  -d '{
    "door_name": "door_2",
    "servo_pin": 27,
    "min_angle": -90,
    "max_angle": 90,
    "min_pulse": 0.0005,
    "max_pulse": 0.0025
  }'
```

**Lösung 3: Fallback auf Standard-Werte**
Der `pi_agent.py` wurde aktualisiert und verwendet nun automatisch Standard-Werte (door_1: Pin 17, door_2: Pin 27), wenn keine Settings aus der API geladen werden können. Der Agent wird nicht mehr beendet, sondern läuft mit diesen Standardwerten weiter.

### Servo-Pins anpassen
Die Standard-Pins sind:
- door_1: GPIO Pin 17
- door_2: GPIO Pin 27

Diese können über die API-Einstellungen angepasst werden, oder in `quick_init.py` vor der Ausführung geändert werden.

### "invalid state 250 for pin GPIOxx"
Dieser Fehler tritt auf, wenn GPIO-Pins bereits von einem anderen Prozess verwendet werden oder in einem ungültigen Zustand sind.

**Lösung 1: GPIO-Pins bereinigen (Empfohlen)**
```bash
python3 cleanup_gpio.py
```
Dies bereinigt die Standard-Pins (17, 18, 27). Für andere Pins:
```bash
python3 cleanup_gpio.py --pins 17 18
```

**Lösung 2: Pi-Agent neu starten**
```bash
# Stoppe den laufenden Agent
sudo pkill -f pi_agent

# Warte kurz
sleep 2

# Starte neu
python3 -m app.pi_agent
```

**Lösung 3: pigpiod neu starten**
```bash
sudo systemctl restart pigpiod
sleep 2
python3 -m app.pi_agent
```

**Lösung 4: Raspberry Pi neu starten**
Wenn alle anderen Lösungen fehlschlagen:
```bash
sudo reboot
```

### pigpiod nicht erreichbar
Stelle sicher, dass der pigpio-Daemon läuft:
```bash
sudo systemctl status pigpiod

# Falls nicht aktiv:
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
```

### "OPTIONS /xyz HTTP/1.1" 405 Method Not Allowed
Dieser Fehler tritt bei CORS-Pre-flight-Requests auf. 

**Lösung: API-Server neu starten**
Nach der CORS-Konfigurationsänderung muss der Server neu gestartet werden:
```bash
# Server stoppen (CTRL+C) und neu starten:
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

Die CORS-Middleware ist nun korrekt konfiguriert mit:
- `allow_origins=["*"]` - Alle Origins erlaubt
- `allow_credentials=False` - Notwendig bei Wildcard-Origins
- `allow_methods=["*"]` - Alle HTTP-Methoden inkl. OPTIONS
- `allow_headers=["*"]` - Alle Header erlaubt

