from fastapi import FastAPI
import uvicorn, logging

from . import models
from .database import engine
from .routers import accounts, login, users
from .config import environment_variable

logging.basicConfig(level=logging.DEBUG, filename='app.log', format="%(asctime)s: %(levelname)s: %(message)s")
# log levels: critical; error; warning; info; debug

models.Base.metadata.create_all(bind=engine)

PassMan = FastAPI()

PassMan.include_router(accounts.router)
PassMan.include_router(users.router)
PassMan.include_router(login.router)

@PassMan.get("/")
def default():
    return {"Message": "Server is up and running..."}

if __name__ == '__main__':

    uvicorn.run(PassMan, host='0.0.0.0', port=8000, debug=True, reload=False, log_level="info", access_log=True)
