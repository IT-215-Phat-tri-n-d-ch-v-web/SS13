from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase


DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/users_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

