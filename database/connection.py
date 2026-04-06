from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, poolclass=NullPool)

def get_session():
    with Session(engine) as session:
        yield session