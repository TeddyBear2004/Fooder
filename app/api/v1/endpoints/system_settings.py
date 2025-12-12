"""
System Settings API Endpoints
REST-Endpunkte für globale System-Einstellungen.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.system_settings import SystemSettings, SystemSettingsUpdate
from app.services import SystemSettingsService

router = APIRouter()
settings_service = SystemSettingsService()


@router.get("", response_model=SystemSettings, summary="System-Einstellungen abrufen")
def get_system_settings(db: Session = Depends(get_db)):
    """
    Gibt die globalen System-Einstellungen zurück.

    Enthält u.a.:
    - pending_door_values: Standard-Türwerte für unbekannte RFIDs

    Returns:
        SystemSettings
    """
    return settings_service.get(db)


@router.put("", response_model=SystemSettings, summary="System-Einstellungen aktualisieren")
def update_system_settings(
    settings_update: SystemSettingsUpdate,
    db: Session = Depends(get_db)
):
    """
    Aktualisiert die globalen System-Einstellungen.

    Alle Felder sind optional - nur angegebene Felder werden aktualisiert.

    Args:
        settings_update: Update-Daten

    Returns:
        Aktualisierte SystemSettings

    Raises:
        400: Validierungsfehler
    """
    try:
        return settings_service.update(db, settings_update)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

