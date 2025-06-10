from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    title = Column(String, nullable=False)
    memo = Column(String, nullable=True)