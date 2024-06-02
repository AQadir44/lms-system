from datetime import timedelta , datetime
from typing import Annotated
from fastapi import APIRouter , Depends , HTTPException
from sqlmodel import SQLModel
from sqlalchemy.orm import Session 
from starlette import status
from .database import SessionLocal , get_db
from .models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer ,     OAuth2PasswordRequestForm
from jose import jwt , JWTError
import os
from dotenv import load_dotenv

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@auth_router.post('/signup' , status_code=status.HTTP_201_CREATED )
async def login_for_access_token(db : Annotated[Session, Depends(get_db)] , user : User):

    password = user.pop['password']
    user_data = User( **user ,
                     password=bcrypt_context.hash(password)) 

    db.add(user_data)
    db.commit()

    return user