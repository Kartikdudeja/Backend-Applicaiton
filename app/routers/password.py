from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import or_
from starlette.status import HTTP_404_NOT_FOUND

from app.database import get_db
from app import models, schemas, oauth2, utils

import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix = "/apigw/password"
)

@router.get("/", response_model=schemas.PasswordOut)
def get_password_by_search(search: str = "", db: Session = Depends(get_db), logged_in: str = Depends(oauth2.get_current_user)):

    # search: platform 
    # search: username

    logger.info(f'Get Password Request Received from User ID: {logged_in.id} with keyword: {search}')

    data_query = db.query(models.Accounts).filter(models.Accounts.owner_id == logged_in.id).filter(or_ (models.Accounts.platform.contains(search), models.Accounts.username.contains(search)))

    data = data_query.first()

    if not data:
        logger.error(f"No Result found with the keyword: {search}")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"No Result found with the keyword: {search}")

    # Decrypt Password
    decypted_pw = utils.decrypt_password(data.password)
    data.password = decypted_pw

    # To-Do: Implement a Logic to Retun Multiple Records
    # map() can be useful
    return data

@router.get("/{id}", response_model=schemas.PasswordOut)
def get_password_by_id(id: int, db: Session = Depends(get_db), logged_in: str = Depends(oauth2.get_current_user)):
    
    logger.info(f'Get Password Request Received from User ID: {logged_in.id} for Account ID: {id}')

    data_query = db.query(models.Accounts).filter(models.Accounts.owner_id == logged_in.id).filter(models.Accounts.id == id)

    data = data_query.first()

    if not data:
        logger.info(f"ID: {id} doesn't exist")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")


    # Decrypt Password
    decypted_pw = utils.decrypt_password(data.password)
    data.password = decypted_pw

    return data