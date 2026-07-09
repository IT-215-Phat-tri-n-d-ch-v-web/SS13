from sqlalchemy.orm import Session
from model import MenuItem

def get_all(db: Session):
    db.query(MenuItem).all()

    return menu