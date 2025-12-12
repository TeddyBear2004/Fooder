"""
Logs API Endpoints
REST-Endpunkte für AccessLog-Verwaltung.
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.access_log import AccessLog, AccessLogCreate
from app.services import LogService

router = APIRouter()
log_service = LogService()


@router.get("", response_model=List[AccessLog], summary="Alle Logs abrufen")
def get_logs(
    limit: int = Query(100, ge=1, le=1000, description="Maximale Anzahl Einträge"),
    entity_id: Optional[int] = Query(None, description="Filter nach Entity-ID"),
    action: Optional[str] = Query(None, description="Filter nach Aktion"),
    db: Session = Depends(get_db)
):
    """
    Gibt Zugriffslogs zurück (neueste zuerst).

    Args:
        limit: Maximale Anzahl Einträge (default: 100, max: 1000)
        entity_id: Optional - Filter nach Entity-ID
        action: Optional - Filter nach Aktion (z.B. 'granted', 'unknown')

    Returns:
        Liste von AccessLog-Einträgen
    """
    if entity_id is not None:
        return log_service.get_by_entity(db, entity_id, limit)
    elif action is not None:
        return log_service.get_by_action(db, action, limit)
    else:
        return log_service.get_all(db, limit)


@router.get("/{log_id}", response_model=AccessLog, summary="Log anhand ID abrufen")
def get_log(log_id: int, db: Session = Depends(get_db)):
    """
    Gibt einen einzelnen Log-Eintrag anhand der ID zurück.

    Args:
        log_id: ID des Logs

    Returns:
        Log-Daten

    Raises:
        404: Log nicht gefunden
    """
    log = log_service.get_by_id(db, log_id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Log mit ID {log_id} nicht gefunden"
        )

    return log


@router.post("", response_model=AccessLog, status_code=status.HTTP_201_CREATED, summary="Neuen Log erstellen")
def create_log(log: AccessLogCreate, db: Session = Depends(get_db)):
    """
    Erstellt einen neuen Log-Eintrag.

    Args:
        log: Log-Daten (entity_id kann null sein für unbekannte RFIDs)

    Returns:
        Erstellter Log-Eintrag
    """
    return log_service.create(db, log)

