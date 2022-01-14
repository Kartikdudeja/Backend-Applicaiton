from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN

from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    prefix="/apigw/login"
)

@router.post("/", response_model=schemas.Token)
def login(users_credentails: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user_query = db.query(models.Users).filter(models.Users.email == users_credentails.username)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail= "Invalid Credentails")

    if not utils.verify_password(users_credentails.password, user.password):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail= "Invalid Credentails")

    access_token = oauth2.create_access_token(data = {"id": user.id, "email": user.email})

    return {"access_token": access_token, "token_type": "bearer", "expires_in": oauth2.ACCESS_TOKEN_EXPIRE_MINUTE * 60}
