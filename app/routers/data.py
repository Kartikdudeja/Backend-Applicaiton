from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from datetime import timedelta

from app.database import get_db, redis_client
from app import models
from app.config import environment_variable

import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/apigw/data"
)

# endpoint to get user details from user id
@router.get("/{id}")
def get_data_by_id(id: int, db: Session = Depends(get_db)):
    
    logger.info(f'Get User Name for ID: {id}')
    # redis call
    res_data = redis_client.get(id)

    if not res_data:

        logger.info("Cache Miss, Quering Database to Retrieve Data")
        # querying database in case details are not found in redis
        data_query = db.query(models.Users).filter(models.Users.id == id)
        data = data_query.first()
        
        if not data:

            logger.error(f"ID: {id} doesn't exist")
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")
        
        res_data = data.email
        # push data to redis
        redis_client.set(id, res_data, timedelta(minutes=environment_variable.REDIS_KEY_EXPIRE_MINUTE))

    else:
       logger.info("Cache Hit")

    if not res_data:

        logger.error(f"ID: {id} doesn't exist")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")

    return {"mail_id": res_data}
