from sqlalchemy.orm import Session
from database import SessionLocal
from schema import Item, ItemCreate
from models import ItemModel

def create_item(item: ItemCreate):
    db = SessionLocal()
    db_item = ItemModel(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item

def get_item_by_id(item_id: int):
    db = SessionLocal()
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    db.close()
    return item
