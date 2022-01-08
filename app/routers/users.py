from fastapi import FastAPI, Depends, APIRouter
from fastapi.exceptions import HTTPException

from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix = "/apigw/users"
)

@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    
    hashed_pw = utils.hash_password(user.password)
    user.password = hashed_pw

    new_user = models.Users(**user.dict())

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=f"{user.email} already exists")

    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), logged_in = Depends(oauth2.get_current_user)):

    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"User with id: {id} doesn't exist")

    return user