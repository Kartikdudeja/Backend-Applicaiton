from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, logging

from app import models
from app.database import engine
from app.routers import accounts, login, users, password, data

logging.basicConfig(level=logging.INFO, filename='app.log', format="%(asctime)s: %(levelname)s: [%(process)d:%(processName)s] (%(filename)s-%(module)s.%(funcName)s): %(message)s")
# log levels: critical; error; warning; info; debug

logger = logging.getLogger(__name__)

# sqlalchemy engine to create database table
models.Base.metadata.create_all(bind=engine)

PassMan = FastAPI()

# CORS Policy
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

PassMan.include_router(accounts.router)
PassMan.include_router(users.router)
PassMan.include_router(login.router)
PassMan.include_router(password.router)
PassMan.include_router(data.router)

@PassMan.get("/")
def default():
    return {"Message": "Server is up and running..."}

def main():
    
    uvicorn.run(PassMan, host='0.0.0.0', port=8000, debug=True, reload=False, log_level="info", access_log=True)

if __name__ == '__main__':

    main()