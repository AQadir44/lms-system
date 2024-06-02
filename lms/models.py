from sqlmodel import Field, SQLModel, create_engine, Session, select
from .database import engine


def create_db_and_tables()->None:
    SQLModel.metadata.create_all(engine)


class Token(SQLModel):
    __tablename__ = "tokens"
    access_token: str
    token_type: str

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True)
    user_name :str = Field(unique=True)
    first_name: str
    last_name: str
    email: str
    country: str
    password: str


class Login(SQLModel):
    username:str
    password : str