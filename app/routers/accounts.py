from fastapi import status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from starlette.responses import Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, HTTP_422_UNPROCESSABLE_ENTITY

from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, schemas, oauth2, utils
from app.database import get_db

import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix = "/apigw/accounts"
)

LIMIT = 10
OFFSET = 0

@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.AccountResponse)
def add_account_details(data: schemas.CreateAccount, db: Session = Depends(get_db), logged_in: str = Depends(oauth2.get_current_user)):

    logger.info(f'New Details Request from User ID: {logged_in.id}')    
    # Encypt  Password before storing in Database
    encypted_pw = utils.encrypt_password(data.password)
    data.password = encypted_pw
    
    new_account = models.Accounts(**data.dict(), owner_id=logged_in.id)

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account

@router.get("/", response_model=List[schemas.AccountResponse])
def get_all_account_details(db: Session = Depends(get_db), logged_in: str = Depends(oauth2.get_current_user), search: Optional[str] = "", limit: int = LIMIT, offset: int = OFFSET):
    
    logger.info(f'Get All Account Details Request from User ID: {logged_in.id}')

    if limit > 10:
        logger.error(f'Limit Error: Parameter Value ({limit}) is greater than defined Threshold')
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="You cannot request more than 10 items")

    accounts_query = db.query(models.Accounts).filter(models.Accounts.owner_id == logged_in.id).filter(models.Accounts.platform.contains(search)).limit(limit).offset(offset)
    
    accounts = accounts_query.all()

    return accounts

@router.get("/{id}", response_model=schemas.AccountResponse)
def get_by_id(id: int, db: Session = Depends(get_db), logged_in: str = Depends(oauth2.get_current_user)):

    logger.info(f'Get Account Details Request from User ID: {logged_in.id} for Account ID: {id}')

    account_query = db.query(models.Accounts).filter(models.Accounts.owner_id == logged_in.id).filter(models.Accounts.id == id)
    account = account_query.first()
        
    if not account: 

        logger.error(f"ID: {id} doesn't exist")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")

    if account.owner_id != logged_in.id:

        logger.error(f'User ID: {logged_in.id} is not authorized to perform requested action')
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")

    return account

@router.put("/{id}")
def update_account_details(id: int, data: schemas.UpdateAccount, db: Session = Depends(get_db), logged_in: str = Depends(oauth2.get_current_user)):
    
    logger.info(f'Update Request Received for Account ID: {id} from Used ID: {logged_in.id}')
    account_query = db.query(models.Accounts).filter(models.Accounts.owner_id == logged_in.id).filter(models.Accounts.id == id)
    account = account_query.first()

    if account == None:

        logger.error(f"ID: {id} doesn't exist")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")

    if account.owner_id != logged_in.id:

        logger.error(f'User ID: {logged_in.id} is not authorized to perform requested action')
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")

    account_query.update(data.dict(), synchronize_session=False)
    db.commit()
    
    return {"status": "Password Updated Successfully"}


@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_account_data(id: int, db: Session = Depends(get_db), logged_in: str = Depends(oauth2.get_current_user)):

    logger.info(f'Delete Request Received for Account ID: {id} from Used ID: {logged_in.id}')
    account_query = db.query(models.Accounts).filter(models.Accounts.owner_id == logged_in.id).filter(models.Accounts.id == id)
    account = account_query.first()

    if account == None: 

        logger.error(f"ID: {id} doesn't exist")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")

    if account.owner_id != logged_in.id:

        logger.error(f'User ID: {logged_in.id} is not authorized to perform requested action')
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")

    account_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=HTTP_204_NO_CONTENT)
