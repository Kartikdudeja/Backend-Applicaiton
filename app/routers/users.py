from asyncio.log import logger
from fastapi import Depends, APIRouter
from fastapi.exceptions import HTTPException

from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import models, schemas, utils, oauth2
from app.database import get_db

import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix = "/apigw/users"
)

@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    
    logger.info(f'New User Request Received with Email id: {user.email}')
    hashed_pw = utils.hash_password(user.password)
    user.password = hashed_pw

    new_user = models.Users(**user.dict())

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f'New User create with Email id: {user.email}')

    except IntegrityError:
        db.rollback()
        logger.error(f'{user.email} already exist')
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=f"{user.email} already exists")
        
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user_by_id(id: int, db: Session = Depends(get_db), logged_in = Depends(oauth2.get_current_user)):

    logger.info(f'Request Received for User details with id: {id}')
    user_query = db.query(models.Users).filter(models.Users.id == logged_in.id).filter(models.Users.id == id)
    user = user_query.first()

    if not user:
        logger.error(f"User with id: {id} doesn't exist")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"User with id: {id} doesn't exist")

    return user