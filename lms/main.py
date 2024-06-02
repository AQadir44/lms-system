from fastapi import FastAPI 
from starlette.middleware.cors import CORSMiddleware
from typing import AsyncGenerator
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from .backend.students import router 
from .models import  create_db_and_tables
from .auth  import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    yield



app = FastAPI(lifespan=lifespan, title="Hello World API with DB", 
    version="0.0.1",
    servers=[
        {
            "url": "http://0.0.0.0:8000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins =origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"], 
)


app.include_router(auth_router)
# app.include_router(router , tags=['SignUp'] , prefix='/api')