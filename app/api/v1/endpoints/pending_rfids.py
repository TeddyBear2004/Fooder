"""
Pending RFIDs API Endpoints
REST-Endpunkte für PendingRFID-Verwaltung (unbekannte RFID-Tags).
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.pending_rfid import PendingRFID, PendingRFIDCreate
from app.schemas.entity import Entity, EntityCreate
from app.services import PendingRFIDService

router = APIRouter()
pending_service = PendingRFIDService()


@router.get("", response_model=List[PendingRFID], summary="Alle unbekannten RFIDs abrufen")
def get_pending_rfids(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Gibt alle unbekannten/nicht-registrierten RFID-Tags zurück.

    Diese Tags wurden gescannt, sind aber noch nicht als Entity registriert.

    Args:
        limit: Maximale Anzahl Einträge (default: 50)

    Returns:
        Liste aller PendingRFID-Einträge (neueste zuerst)
    """
    return pending_service.get_all(db, limit)


@router.get("/{pending_id}", response_model=PendingRFID, summary="PendingRFID anhand ID abrufen")
def get_pending_rfid(pending_id: int, db: Session = Depends(get_db)):
    """
    Gibt einen einzelnen PendingRFID anhand der ID zurück.

    Args:
        pending_id: ID des PendingRFID

    Returns:
        PendingRFID-Daten

    Raises:
        404: PendingRFID nicht gefunden
    """
    pending = pending_service.get_by_id(db, pending_id)
    if not pending:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"PendingRFID mit ID {pending_id} nicht gefunden"
        )

    return pending


@router.post("", response_model=PendingRFID, status_code=status.HTTP_201_CREATED, summary="RFID manuell als 'pending' markieren")
def create_pending_rfid(pending: PendingRFIDCreate, db: Session = Depends(get_db)):
    """
    Markiert einen RFID-Tag manuell als "pending" (unbekannt).

    Normalerweise erfolgt dies automatisch beim Scannen.

    Args:
        pending: PendingRFID-Daten

    Returns:
        Erstellter PendingRFID
    """
    return pending_service.register_unknown_rfid(db, pending.rfid_id)


@router.post("/{pending_id}/convert", response_model=Entity, summary="PendingRFID zu Entity konvertieren")
def convert_pending_to_entity(
    pending_id: int,
    entity: EntityCreate,
    db: Session = Depends(get_db)
):
    """
    Konvertiert einen PendingRFID zu einer vollständigen Entity.

    Die RFID-ID aus dem Entity muss mit der des PendingRFID übereinstimmen.
    Nach erfolgreicher Konvertierung wird der PendingRFID gelöscht.

    Args:
        pending_id: ID des PendingRFID
        entity: Entity-Daten (inkl. door_values)

    Returns:
        Neu erstellte Entity

    Raises:
        404: PendingRFID nicht gefunden
        400: RFID-ID Mismatch oder bereits registriert
    """
    try:
        converted = pending_service.convert_to_entity(db, pending_id, entity)
        if not converted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"PendingRFID mit ID {pending_id} nicht gefunden"
            )

        return converted

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{pending_id}", summary="PendingRFID löschen")
def delete_pending_rfid(pending_id: int, db: Session = Depends(get_db)):
    """
    Löscht einen PendingRFID ohne zu konvertieren.

    Nützlich wenn der RFID-Scan ein Fehler war oder nicht benötigt wird.

    Args:
        pending_id: ID des PendingRFID

    Returns:
        Erfolgsmeldung

    Raises:
        404: PendingRFID nicht gefunden
    """
    pending = pending_service.delete(db, pending_id)
    if not pending:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"PendingRFID mit ID {pending_id} nicht gefunden"
        )

    return {"detail": f"PendingRFID {pending_id} erfolgreich gelöscht"}

