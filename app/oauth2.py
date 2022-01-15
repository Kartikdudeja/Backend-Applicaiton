from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm.session import Session

from starlette.status import HTTP_401_UNAUTHORIZED

from app import database, schemas, models
from app.config import environment_variable

import logging

logger = logging.getLogger(__name__)

oauth_schema = OAuth2PasswordBearer(tokenUrl='apigw/login')

# openssl rand -hex 32 // Generate random string
SECRET_KEY = environment_variable.SECRET_KEY
ALGORITHM = environment_variable.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTE = environment_variable.ACCESS_TOKEN_EXPIRE_MINUTE

def create_access_token(data: dict):
    
    logger.info(f'Create Access Token Request Received for User ID: {data}')
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentail_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: int = payload.get("id")
        email: str = payload.get("email")

        logger.info(f'Verifying Access Token for the User ID: {id}')

        if ((id is None) or (email is None)):
            logger.error(f'Invalid Token; id: {id}, email: {email}')
            raise credentail_exception

        token_data = schemas.TokenData(id=id, email=email)

    except JWTError:
        logger.error("JWT Exception")
        raise credentail_exception

    return token_data

def get_current_user(token: str = Depends(oauth_schema), db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate Credentials", headers={"WWW-Authenticate": "Bearer"})

    logger.info(f'Checking Logged in User with Token: {token}')
    token = verify_access_token(token, credentials_exception)
    user_query = db.query(models.Users).filter(models.Users.id == token.id)
    user = user_query.first()

    return user