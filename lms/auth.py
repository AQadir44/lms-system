from datetime import timedelta , datetime , timezone
from typing import Annotated
from fastapi import APIRouter , Depends , HTTPException 
from sqlmodel import SQLModel
from sqlalchemy.orm import Session 
from starlette import status
from .models import User , Token
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer ,     OAuth2PasswordRequestForm
from jose import jwt , JWTError
import os
from dotenv import load_dotenv
from .database import get_db
from jose import JWTError
from .main import *



load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def authenticate_user(username , password , db : Session):
    user = db.query(User).filter(User.user_name == username).first()
    
    if not user:
        raise False
    
    if not bcrypt_context.verify(password , user.password):
        raise False
    
    return user
    
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str , Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        if username is None and user_id is None:
            raise credentials_exception
        return {"username": username , "id" : user_id}
    except JWTError:
        raise credentials_exception
    
    
    
auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@auth_router.post('/signup' , status_code=status.HTTP_201_CREATED )
async def login_for_access_token(db : Annotated[Session, Depends(get_db)] , user : User):

    
    user.password = bcrypt_context.hash(user.model_dump()['password'])
    
    user_data = User( **user.model_dump() ) 

    db.add(user_data)
    db.commit()
    
    
    return {"message" : "Successfully created account"}

@auth_router.post('/token' , response_model=Token)
async def login_for_access_token(db : Annotated[Session, Depends(get_db)] , form_data : Annotated[OAuth2PasswordRequestForm, Depends()]):

    user = authenticate_user(form_data.username , form_data.password , db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Invalid Credentials")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.user_name , "id" : user.id.hex}, expires_delta=access_token_expires)


    return {"access_token": access_token, "token_type": "bearer"}
