from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Bạn vui lòng cập nhật lại user, password và db_name phù hợp với cấu hình MySQL cục bộ
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/pet_boarding_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()