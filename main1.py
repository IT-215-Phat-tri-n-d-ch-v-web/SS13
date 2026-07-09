from fastapi import FastAPI
from model import MenuItem
from database import Base, engine


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app 