from sqlalchemy import Column, ForeignKey, Integer, String, Date
from .database import Base

class GolfTrainingDB(Base):
    __tablename__ = "golftraining_db"
    date = Column(Date)
    golfclub = Column(String)
    training_id = Column(Integer, primary_key = True, index=True)
