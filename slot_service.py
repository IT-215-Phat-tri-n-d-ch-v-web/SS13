from sqlalchemy.orm import Session
from model2 import BoardingSlot
from schemas2 import BoardingSlotCreate, BoardingSlotUpdate

def get_boarding_slots(db: Session):
    return db.query(BoardingSlot).all()

def get_boarding_slot(db: Session, slot_id: int):
    return db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()

def get_boarding_slot_by_number(db: Session, slot_number: str):
    return db.query(BoardingSlot).filter(BoardingSlot.slot_number == slot_number).first()

def create_boarding_slot(db: Session, slot: BoardingSlotCreate):
    db_slot = BoardingSlot(**slot.model_dump())
    try:
        db.add(db_slot)
        db.commit()
        db.refresh(db_slot)
        return db_slot
    except Exception as e:
        db.rollback()
        raise e

def update_boarding_slot(db: Session, db_slot: BoardingSlot, slot_update: BoardingSlotUpdate):
    # Trích xuất dữ liệu thực tế được truyền lên qua exclude_unset=True
    update_data = slot_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_slot, key, value)
    try:
        db.commit()
        db.refresh(db_slot)
        return db_slot
    except Exception as e:
        db.rollback()
        raise e

def delete_boarding_slot(db: Session, db_slot: BoardingSlot):
    try:
        db.delete(db_slot)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e