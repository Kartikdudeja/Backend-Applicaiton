from typing import List
from fastapi import FastAPI, status, Depends
from fastapi.exceptions import HTTPException
import uvicorn, logging

from starlette.responses import Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

logging.basicConfig(level=logging.DEBUG, filename='app.log', format="%(asctime)s: %(levelname)s: %(message)s")
# log levels: critical; error; warning; info; debug

models.Base.metadata.create_all(bind=engine)

PassMan = FastAPI()

@PassMan.get("/")
def default():
    return {"Message": "Server is up and running..."}

@PassMan.post("/apigw/accounts", status_code=HTTP_201_CREATED, response_model=schemas.AccountResponse)
def add_account_details(data: schemas.CreateAccount, db: Session = Depends(get_db)):

    new_account = models.Accounts(**data.dict())

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account

@PassMan.get("/apigw/accounts", response_model=List[schemas.AccountResponse]) 
def get_account_details(db: Session = Depends(get_db)):

    accounts = db.query(models.Accounts).all()
    return accounts

@PassMan.get("/apigw/accounts/{id}", response_model=schemas.AccountResponse)
def get_by_id(id: int, db: Session = Depends(get_db)):

    account = db.query(models.Accounts).filter(models.Accounts.id == id).first()

    if not account: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")

    return account

@PassMan.put("/apigw/accounts/{id}")
def update_account_details(id: int, data: schemas.UpdateAccount, db: Session = Depends(get_db)):
    
    account_query = db.query(models.Accounts).filter(models.Accounts.id == id)
    account = account_query.first()

    if account == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")

    account_query.update(data.dict(), synchronize_session=False)
    db.commit()

    return {"status": "Password Updated Successfully"}


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
    