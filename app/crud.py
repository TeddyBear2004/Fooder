from sqlalchemy.orm import Session
from . import models, schemas


def get_entities(db: Session):
    return db.query(models.Entity).all()


def get_entity(db: Session, entity_id: int):
    return db.query(models.Entity).filter(models.Entity.id == entity_id).first()


def create_entity(db: Session, entity: schemas.EntityCreate):
    db_entity = models.Entity(**entity.dict())
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity


def update_entity(db: Session, entity_id: int, entity: schemas.EntityCreate):
    db_entity = get_entity(db, entity_id)
    if not db_entity:
        return None
    for key, value in entity.dict().items():
        setattr(db_entity, key, value)
    db.commit()
    db.refresh(db_entity)
    return db_entity


def delete_entity(db: Session, entity_id: int):
    db_entity = get_entity(db, entity_id)
    if not db_entity:
        return None
    db.delete(db_entity)
    db.commit()
    return db_entity


def get_settings(db: Session):
    return db.query(models.DoorSetting).all()


def get_setting(db: Session, setting_id: int):
    return db.query(models.DoorSetting).filter(models.DoorSetting.id == setting_id).first()


def create_setting(db: Session, setting: schemas.DoorSettingCreate):
    db_setting = models.DoorSetting(**setting.dict())
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting


def update_setting(db: Session, setting_id: int, setting: schemas.DoorSettingCreate):
    db_setting = get_setting(db, setting_id)
    if not db_setting:
        return None
    for key, value in setting.dict().items():
        setattr(db_setting, key, value)
    db.commit()
    db.refresh(db_setting)
    return db_setting


def delete_setting(db: Session, setting_id: int):
    db_setting = get_setting(db, setting_id)
    if not db_setting:
        return None
    db.delete(db_setting)
    db.commit()
    return db_setting


def create_log(db: Session, log: schemas.AccessLogCreate):
    db_log = models.AccessLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def get_logs(db: Session):
    return db.query(models.AccessLog).all()
