"""
Settings API Endpoints
REST-Endpunkte für DoorSetting-Verwaltung.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.door_setting import DoorSetting, DoorSettingCreate
from app.services import SettingService

router = APIRouter()
setting_service = SettingService()


@router.get("", response_model=List[DoorSetting], summary="Alle Settings abrufen")
def get_settings(db: Session = Depends(get_db)):
    """
    Gibt alle Tür-Settings zurück.

    Returns:
        Liste aller DoorSettings
    """
    return setting_service.get_all(db)


@router.get("/{setting_id}", response_model=DoorSetting, summary="Setting anhand ID abrufen")
def get_setting(setting_id: int, db: Session = Depends(get_db)):
    """
    Gibt ein einzelnes Setting anhand der ID zurück.

    Args:
        setting_id: ID des Settings

    Returns:
        Setting-Daten

    Raises:
        404: Setting nicht gefunden
    """
    setting = setting_service.get_by_id(db, setting_id)
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Setting mit ID {setting_id} nicht gefunden"
        )

    return setting


@router.post("", response_model=DoorSetting, status_code=status.HTTP_201_CREATED, summary="Neues Setting erstellen")
def create_setting(setting: DoorSettingCreate, db: Session = Depends(get_db)):
    """
    Erstellt ein neues Tür-Setting.

    Args:
        setting: Setting-Daten

    Returns:
        Erstelltes Setting

    Raises:
        400: Tür-Name existiert bereits oder Validierungsfehler
    """
    try:
        return setting_service.create(db, setting)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{setting_id}", response_model=DoorSetting, summary="Setting aktualisieren")
def update_setting(setting_id: int, setting: DoorSettingCreate, db: Session = Depends(get_db)):
    """
    Aktualisiert ein existierendes Setting.

    Args:
        setting_id: ID des Settings
        setting: Neue Setting-Daten

    Returns:
        Aktualisiertes Setting

    Raises:
        404: Setting nicht gefunden
        400: Validierungsfehler
    """
    try:
        updated_setting = setting_service.update(db, setting_id, setting)
        if not updated_setting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Setting mit ID {setting_id} nicht gefunden"
            )

        return updated_setting
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{setting_id}", summary="Setting löschen")
def delete_setting(setting_id: int, db: Session = Depends(get_db)):
    """
    Löscht ein Setting.

    Args:
        setting_id: ID des Settings

    Returns:
        Erfolgsmeldung

    Raises:
        404: Setting nicht gefunden
    """
    setting = setting_service.delete(db, setting_id)
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Setting mit ID {setting_id} nicht gefunden"
        )

    return {"detail": f"Setting {setting_id} erfolgreich gelöscht"}

