# database.py


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.config import Config
from starlette.datastructures import Secret
from sqlmodel import SQLModel, create_engine
import os
from dotenv import load_dotenv


load_dotenv()
SQLALCHEMY_DATABASE_URL= os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL , pool_recycle=300)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
    