from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, oauth2
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm.session import Session

from starlette.status import HTTP_401_UNAUTHORIZED

from app import database, schemas, models

oauth_schema = OAuth2PasswordBearer(tokenUrl='apigw/login')

# openssl rand -hex 32 // Generate random string
SECRET_KEY = "21de31bb6d8d924056a0089f6f49680b0e9e14ee906c8a0444b0a155d74821b8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 60

def create_access_token(data: dict):
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentail_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: int = payload.get("user_id")
        email: str = payload.get("email")

        if id is None or email is None:
            raise credentail_exception
        token_data = schemas.TokenData(id=id, email=email)

    except JWTError:
        raise credentail_exception

    return token_data

def get_current_user(token: str = Depends(oauth_schema), db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate Credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.Users.id == token.id).first()

    return user

