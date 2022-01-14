from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from datetime import timedelta

from ..database import get_db, redis_client
from .. import models
from ..config import environment_variable

router = APIRouter(
    prefix="/apigw/data"
)

@router.get("/{id}")
def get_data_by_id(id: int, db: Session = Depends(get_db)):
    
    res_data = redis_client.get(id)

    if not res_data:

        print("Cache Miss, Quering Database to Retrieve Data")
        data_query = db.query(models.Users).filter(models.Users.id == id)

        data = data_query.first()
        res_data = data.email
        redis_client.set(id, res_data, timedelta(minutes=environment_variable.REDIS_KEY_EXPIRE_MINUTE))

    else:
       print("Cache Hit")

    if not res_data:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")

    return {"mail_id": res_data}
