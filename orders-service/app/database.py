from sqlmodel import create_engine, SQLModel, Session
import os

# Toto se později přesune do .env souboru
DATABASE_URL = "postgresql://user:password@localhost:5432/orders_db"

engine = create_engine(DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
