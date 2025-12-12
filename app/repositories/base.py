"""
Base Repository
Abstrakte Basis-Klasse für alle Repositories mit generischen CRUD-Operationen.
"""
from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.orm import Session
from ..database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generisches Repository für CRUD-Operationen.

    Attributes:
        model: SQLAlchemy-Modell-Klasse
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_all(self, db: Session) -> List[ModelType]:
        """Gibt alle Einträge zurück."""
        return db.query(self.model).all()

    def get_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        """Gibt einen Eintrag anhand der ID zurück."""
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, obj_data: dict) -> ModelType:
        """Erstellt einen neuen Eintrag."""
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, id: int, obj_data: dict) -> Optional[ModelType]:
        """Aktualisiert einen existierenden Eintrag."""
        db_obj = self.get_by_id(db, id)
        if not db_obj:
            return None

        for key, value in obj_data.items():
            setattr(db_obj, key, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> Optional[ModelType]:
        """Löscht einen Eintrag."""
        db_obj = self.get_by_id(db, id)
        if not db_obj:
            return None

        db.delete(db_obj)
        db.commit()
        return db_obj

