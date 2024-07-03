from sqlmodel import Field, SQLModel, create_engine, Session, select , Column , Relationship
from .database import engine
import uuid
from datetime import datetime
from sqlalchemy.dialects import postgresql as pg

def create_db_and_tables()->None:
    SQLModel.metadata.create_all(engine)


class Token(SQLModel):
    __tablename__ = "tokens"
    access_token: str
    token_type: str

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(sa_column=Column(pg.UUID , default=uuid.uuid4, primary_key=True))
    user_name :str = Field(unique=True)
    first_name: str
    last_name: str
    email: str
    country: str
    password: str
    created_at : datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True) , default=datetime.now()))
    is_verified : bool = False


class Login(SQLModel):
    username:str
    password : str
    
    
class Course(SQLModel):
    __tablename__ = "courses"
    id :int = Field(default=None, primary_key=True)
    title : str
    description : str
    duration : int
    created_at : datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True) , default=datetime.now()))
    