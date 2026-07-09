from sqlalchemy.orm import Session
from model import MenuItem
from schemas import MenuItemCreate, MenuItemUpdate

def get_menu_items(db: Session):
    return db.query(MenuItem).all()

def get_menu_item(db: Session, item_id: int):
    return db.query(MenuItem).filter(MenuItem.id == item_id).first()

def get_menu_item_by_code(db: Session, dish_code: str):
    return db.query(MenuItem).filter(MenuItem.dish_code == dish_code).first()

def create_menu_item(db: Session, item: MenuItemCreate):
    db_item = MenuItem(**item.model_dump())
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        db.rollback()
        raise e

def update_menu_item(db: Session, db_item: MenuItem, item_update: MenuItemUpdate):
    update_data = item_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    try:
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        db.rollback()
        raise e

def delete_menu_item(db: Session, db_item: MenuItem):
    try:
        db.delete(db_item)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e