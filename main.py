# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.src.config.database import SessionLocal, Base, engine
from app.src.models.models import Item
from app.src.crud.crud import get_item, create_item
from pydantic import BaseModel

# Tworzenie tabel w bazie danych
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Definicje modeli Pydantic
class ItemCreate(BaseModel):
    name: str
    description: str

class ItemRead(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True

# Funkcja zależności do uzyskania sesji bazy danych
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items/", response_model=ItemRead)
def create_item_view(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db=db, name=item.name, description=item.description)

@app.get("/items/{item_id}", response_model=ItemRead)
def read_item_view(item_id: int, db: Session = Depends(get_db)):
    db_item = get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item