from sqlalchemy.orm import Session

from . import models, schemas

from sqlalchemy import select
from sqlalchemy.engine import Result

def get_training(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.GolfTrainingDB).offset(skip).limit(limit).all()


def create_training(db: Session, trainingapi: schemas.Training):
    db_trainingapi = models.GolfTrainingDB(
        date = trainingapi.date,
        golfclub = trainingapi.golfclub
        )
    db.add(db_trainingapi)
    db.commit()
    db.refresh(db_trainingapi)
    return db_trainingapi

def get_training2(db: Session, training_id: int) -> models.GolfTrainingDB | None:
    result: Result = db.execute(
        select(models.GolfTrainingDB).filter(models.GolfTrainingDB.training_id == training_id)
    )
    return result.scalars().first()


def update_training(db: Session, task_create: schemas.Create_Training, original: models.GolfTrainingDB):
    original.date = task_create.date
    original.golfclub = task_create.golfclub
    db.add(original)
    db.commit()
    db.refresh(original)
    return original


def delete_training(db: Session, original: models.GolfTrainingDB):
    db.delete(original)
    db.commit()