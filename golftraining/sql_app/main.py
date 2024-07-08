from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import sessionLocal, engine

from typing import List

#DBの作成
models.Base.metadata.create_all(bind=engine)

# FastAPIインスタンスの作成
app = FastAPI()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/training", response_model=List[schemas.Training])
def get_training(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    training_list = crud.get_training(db, skip=skip, limit=limit)
    return training_list


@app.post("/training", response_model=schemas.Training)
def post_training(training: schemas.Create_Training, db: Session = Depends(get_db)):
    return crud.create_training(db=db, trainingapi=training)

@app.put("/training/{training_id}", response_model=schemas.Training)
#試しにschemas.Trainingで実験
#training_idは数値、training_bodyはdateとgolfclub
def update_training(training_id: int, training_body: schemas.Create_Training, db: Session = Depends(get_db)):
    training = crud.get_training2(db, training_id=training_id)
    if training is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_training(db, task_create=training_body, original=training)


@app.delete("/training/{training_id}", response_model=None)
#@app.delete("/training{training_id}", response_model=None)
def delete_training(training_id: int, db: Session = Depends(get_db)):
    training = crud.get_training2(db=db, training_id=training_id)
    if training is None:
        raise HTTPException(status_code=404, detail="Training not found")
    
    return crud.delete_training(db, original=training)