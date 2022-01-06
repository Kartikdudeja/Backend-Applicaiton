from os import sync
from fastapi import FastAPI, status, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
import time, logging

import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.sql.functions import mode

from starlette.responses import Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

import uvicorn

from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

logging.basicConfig(level=logging.DEBUG, filename='app.log', format="%(asctime)s: %(levelname)s: %(message)s")
# log levels: critical; error; warning; info; debug

models.Base.metadata.create_all(bind=engine)

PassMan = FastAPI()

class Data (BaseModel):
    platform: str
    username: str
    password: str

@PassMan.get("/")
def default():
    return {"Message": "Server is up and running..."}

@PassMan.post("/apigw/accounts", status_code=HTTP_201_CREATED)
def add_account_details(data: Data, db: Session = Depends(get_db)):

    new_account = models.Accounts(**data.dict())

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return {"New Details Added": new_account }

@PassMan.get("/apigw/accounts")
def get_account_details(db: Session = Depends(get_db)):

    accounts = db.query(models.Accounts).all()

    return { "data": accounts }

@PassMan.get("/apigw/accounts/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):

    account = db.query(models.Accounts).filter(models.Accounts.id == id).first()

    if not account: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")

    return { "Requested Data": account }

@PassMan.put("/apigw/accounts/{id}")
def update_account_details(id: int, data: Data, db: Session = Depends(get_db)):
    
    account_query = db.query(models.Accounts).filter(models.Accounts.id == id)
    account = account_query.first()

    if account == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")

    account_query.update(data.dict(), synchronize_session=False)
    db.commit()

    return {"Updated Details": account_query.first() }


@PassMan.delete("/apigw/accounts/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_account_data(id: int, db: Session = Depends(get_db)):
    
    account = db.query(models.Accounts).filter(models.Accounts.id == id)

    if account.first() == None: 
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")

    account.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=HTTP_204_NO_CONTENT)

if __name__ == '__main__':

    uvicorn.run(PassMan, host='0.0.0.0', port=8000, debug=True, reload=False, log_level="info", access_log=True)
    