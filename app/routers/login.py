from asyncio.log import logger
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN

from app import database, schemas, models, utils, oauth2

import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/apigw/login"
)

# check if a valid user or not, if valid, return authentication token
@router.post("/", response_model=schemas.Token)
def login(users_credentails: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    logger.info(f'Login Request Received for the User: {users_credentails.username}')
    #query database to check for user id received in jwt auth token
    user_query = db.query(models.Users).filter(models.Users.email == users_credentails.username)
    user = user_query.first()

    if not user:
        logger.error("Invalid Credentails")
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail= "Invalid Credentails")

    if not utils.verify_password(users_credentails.password, user.password):
        logger.error("Invalid Credentails")
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail= "Invalid Credentails")

    # create token for valid user
    access_token = oauth2.create_access_token(data = {"id": user.id, "email": user.email})

    jwt_token = {"access_token": access_token, "token_type": "bearer", "expires_in": oauth2.ACCESS_TOKEN_EXPIRE_MINUTE * 60}

    logger.info(f'Access Token created for the User: {user.email}')

    return jwt_token
