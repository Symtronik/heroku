# app/src/models/models.py
from sqlalchemy import Column, Integer, String
from app.src.config.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)