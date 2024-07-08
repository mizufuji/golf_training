from pydantic import BaseModel
from datetime import date

class Create_Training(BaseModel):
    date: date
    golfclub: str

class Training(Create_Training):
    training_id: int

    class Config:
        orm_mode = True