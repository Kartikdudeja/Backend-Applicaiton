from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app import models
from app.database import engine
from app.routers import accounts, login, users, password, data

logging.basicConfig(level=logging.INFO, filename='app.log', format="%(asctime)s: %(levelname)s: [%(process)d:%(processName)s] (%(filename)s-%(module)s.%(funcName)s): %(message)s")
# log levels: critical; error; warning; info; debug

logger = logging.getLogger(__name__)

# sqlalchemy engine to create database table
models.Base.metadata.create_all(bind=engine)

# PassMan is an instance of Fast API framework
PassMan = FastAPI()

# CORS Policy for allowing request from different domains
origins = [
    "http://localhost",
    "https://localhost:",
]

PassMan.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)

# Routers for routing request to different endpoints
PassMan.include_router(accounts.router)
PassMan.include_router(users.router)
PassMan.include_router(login.router)
PassMan.include_router(password.router)
PassMan.include_router(data.router)

# Default Endpoint
@PassMan.get("/")
def default():
    return {"Message": "Server is up and running..."}
