from fastapi import FastAPI 
from starlette.middleware.cors import CORSMiddleware
from typing import AsyncGenerator
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from .backend.course import router 
from .models import  create_db_and_tables
from typing import Annotated
from fastapi import Depends , HTTPException
from .database import get_db
from sqlalchemy.orm import Session 
from starlette import status
from .auth  import auth_router , get_current_user
from aiokafka import AIOKafkaProducer , AIOKafkaConsumer
import asyncio
import json

from lms import course_pb2

async def consumer(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(topic, bootstrap_servers=bootstrap_servers, group_id="my-group" , auto_offset_reset="earliest")
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Message {msg.value.code()} for topic {msg.topic}")
    finally:
        await consumer.stop()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    
    task = asyncio.create_task(consumer("User_topic", "broker:19092"))
    create_db_and_tables()
    yield
  
user_dependency = Annotated[dict ,  Depends(get_current_user)]



app = FastAPI(lifespan=lifespan, title="Hello World API with DB", 
    version="0.0.1")

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


# app.include_router(auth_router)
app.include_router(auth_router )
app.include_router(router, prefix="/courses", tags=["Courses"])

async def get_kafka_producer():
    producer = AIOKafkaProducer(    
        bootstrap_servers="broker:19092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
        

@app.get("/users/me/" , status_code=status.HTTP_200_OK)
async def read_users_me(user : user_dependency , db : Annotated[Session, Depends(get_db)] , producer : Annotated[AIOKafkaProducer, Depends(get_kafka_producer)] ):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Invalid Credentials")
    await producer.send_and_wait("User_topic", {"user" : user})
    return {"user" : user}

