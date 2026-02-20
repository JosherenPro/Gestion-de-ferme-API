import os
from sqlmodel import SQLModel, create_engine, Session
from app.core.config import DATABASE_URL, DEBUG



# echo = True pour le debug
engine = create_engine(DATABASE_URL, echo=DEBUG)

def init_db():
    SQLModel.metadata.create_all(engine)
 

def get_session():
    with Session(engine) as session:
        yield session