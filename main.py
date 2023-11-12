import os.path

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, SessionLocal

if not os.path.exists('.\sqlitedb'):
    os.makedirs('.\sqlitedb')

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET endpoint to retrieve all drinks
@app.get("/drinks/", response_model=list[schemas.Drink])
def get_drinks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_drinks(db, skip=skip, limit=limit)

# GET endpoint to retrieve all stock
@app.get("/stock/", response_model=list[schemas.Stock])
def get_stock(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_stock(db, skip=skip, limit=limit)

# DELETE endpoint to delete a specific drink by ID
@app.delete("/drinks/{drink_id}")
def delete_drink_endpoint(drink_id: int, db: Session = Depends(get_db)):
    crud.delete_drink(db, drink_id)
    return {"message": "Drink deleted successfully"}

# POST endpoint to create a new drink
@app.post("/drinks/", response_model=schemas.Drink)
def create_drink(drink: schemas.DrinkCreate, db: Session = Depends(get_db)):
    return crud.create_drink(db, drink)

@app.post("/stock/{drink_id}", response_model=schemas.Stock)
def create_stock(drink_id: int, stock: schemas.StockCreate, db: Session = Depends(get_db)):
    return crud.create_stock(db, stock, drink_id)
