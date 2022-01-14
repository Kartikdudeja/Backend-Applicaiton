from typing import List, Optional
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import or_
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from app.database import get_db
from app import models, schemas, oauth2, utils

router = APIRouter(
    prefix = "/apigw/password"
)

@router.get("/", response_model=schemas.PasswordOut)
def get_password_by_search(search: Optional [str] = "", db: Session = Depends(get_db), logged_in: str = Depends(oauth2.get_current_user)):

    # To-Do: Authorized before running Query in DB

    data_query = db.query(models.Accounts).filter(or_(models.Accounts.platform.contains(search), models.Accounts.username.contains(search)))
    
    # .like() or .contain() for the keyword search

    data = data_query.first()

    if not data:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"No Result found with the keyword: {search}")


    if data.owner_id != logged_in.id:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")

    # Decrypt Password
    decypted_pw = utils.decrypt_password(data.password)
    data.password = decypted_pw

    return data

@router.get("/{id}", response_model=schemas.PasswordOut)
def get_password_by_id(id: int, db: Session = Depends(get_db), logged_in: str = Depends(oauth2.get_current_user)):
    
    # To-Do: Authorized before running Query in DB

    data_query = db.query(models.Accounts).filter(and_(models.Accounts.owner_id == logged_in.id, models.Accounts.id == id))

    #data_query = db.query(models.Accounts).filter(models.Accounts.id == id)
    data = data_query.first()

    if not data:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")

    if data.owner_id != logged_in.id:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")

    # Decrypt Password
    decypted_pw = utils.decrypt_password(data.password)
    data.password = decypted_pw

    return data