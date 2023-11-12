from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Drink, Stock
from schemas import DrinkCreate, StockCreate


def get_drinks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Drink).offset(skip).limit(limit).all()

def create_drink(db: Session, drink: DrinkCreate):
    db_drink = Drink(**drink.dict())
    db.add(db_drink)
    db.commit()
    db.refresh(db_drink)
    return db_drink

def get_stock(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Stock).offset(skip).limit(limit).all()

def create_stock(db: Session, stock: StockCreate, drink_id: int):
    db_stock = Stock(**stock.dict(), drink_id=drink_id)
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def delete_drink(db: Session, drink_id: int):
    db_drink = db.query(Drink).filter(Drink.id == drink_id).first()
    if db_drink is None:
        raise HTTPException(status_code=404, detail="Drink not found")

    # Delete the associated stock entry
    db_stock = db.query(Stock).filter(Stock.drink_id == drink_id).first()
    if db_stock:
        db.delete(db_stock)

    db.delete(db_drink)
    db.commit()
