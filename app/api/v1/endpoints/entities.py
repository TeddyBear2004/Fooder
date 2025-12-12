"""
Entities API Endpoints
REST-Endpunkte für Entity-Verwaltung.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.entity import Entity, EntityCreate
from app.schemas.access_log import AccessLogCreate
from app.services import EntityService, LogService

router = APIRouter()
entity_service = EntityService()
log_service = LogService()


@router.get("", response_model=List[Entity], summary="Alle Entities abrufen")
def get_entities(db: Session = Depends(get_db)):
    """
    Gibt alle registrierten Entities zurück.

    Returns:
        Liste aller Entities
    """
    return entity_service.get_all(db)


@router.get("/{entity_id}", response_model=Entity, summary="Entity anhand ID abrufen")
def get_entity(entity_id: int, db: Session = Depends(get_db)):
    """
    Gibt eine einzelne Entity anhand der ID zurück.

    Args:
        entity_id: ID der Entity

    Returns:
        Entity-Daten

    Raises:
        404: Entity nicht gefunden
    """
    entity = entity_service.get_by_id(db, entity_id)
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entity mit ID {entity_id} nicht gefunden"
        )

    # Logge den Zugriff
    log_service.log_access(db, entity_id, "read")

    return entity


@router.post("", response_model=Entity, status_code=status.HTTP_201_CREATED, summary="Neue Entity erstellen")
def create_entity(entity: EntityCreate, db: Session = Depends(get_db)):
    """
    Erstellt eine neue Entity.

    Args:
        entity: Entity-Daten

    Returns:
        Erstellte Entity

    Raises:
        400: RFID-ID existiert bereits
    """
    try:
        return entity_service.create(db, entity)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{entity_id}", response_model=Entity, summary="Entity aktualisieren")
def update_entity(entity_id: int, entity: EntityCreate, db: Session = Depends(get_db)):
    """
    Aktualisiert eine existierende Entity.

    Args:
        entity_id: ID der Entity
        entity: Neue Entity-Daten

    Returns:
        Aktualisierte Entity

    Raises:
        404: Entity nicht gefunden
        400: Validierungsfehler
    """
    try:
        updated_entity = entity_service.update(db, entity_id, entity)
        if not updated_entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Entity mit ID {entity_id} nicht gefunden"
            )

        # Logge die Aktualisierung
        log_service.log_access(db, entity_id, "update")

        return updated_entity
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{entity_id}", summary="Entity löschen")
def delete_entity(entity_id: int, db: Session = Depends(get_db)):
    """
    Löscht eine Entity.

    Args:
        entity_id: ID der Entity

    Returns:
        Erfolgsmeldung

    Raises:
        404: Entity nicht gefunden
    """
    entity = entity_service.delete(db, entity_id)
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entity mit ID {entity_id} nicht gefunden"
        )

    # Logge die Löschung
    log_service.log_access(db, entity_id, "delete")

    return {"detail": f"Entity {entity_id} erfolgreich gelöscht"}

