from fastapi import FastAPI, status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRoute
from starlette.responses import Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix = "/apigw/accounts"
)

@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.AccountResponse)
def add_account_details(data: schemas.CreateAccount, db: Session = Depends(get_db), logged_in = Depends(oauth2.get_current_user)):

    new_account = models.Accounts(**data.dict())

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account

@router.get("/", response_model=List[schemas.AccountResponse])
def get_account_details(db: Session = Depends(get_db), logged_in = Depends(oauth2.get_current_user)):
    accounts = db.query(models.Accounts).all()
    return accounts

@router.get("/{id}", response_model=schemas.AccountResponse)
def get_by_id(id: int, db: Session = Depends(get_db), logged_in = Depends(oauth2.get_current_user)):

    account = db.query(models.Accounts).filter(models.Accounts.id == id).first()

    if not account: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")

    return account

@router.put("/{id}")
def update_account_details(id: int, data: schemas.UpdateAccount, db: Session = Depends(get_db), logged_in = Depends(oauth2.get_current_user)):
    
    account_query = db.query(models.Accounts).filter(models.Accounts.id == id)
    account = account_query.first()

    if account == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")

    account_query.update(data.dict(), synchronize_session=False)
    db.commit()

    return {"status": "Password Updated Successfully"}


@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_account_data(id: int, db: Session = Depends(get_db), logged_in = Depends(oauth2.get_current_user)):
    
    account = db.query(models.Accounts).filter(models.Accounts.id == id)

    if account.first() == None: 
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")

    account.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=HTTP_204_NO_CONTENT)
