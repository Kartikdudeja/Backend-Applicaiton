from fastapi import FastAPI, status, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
import time, logging

import psycopg2
from psycopg2.extras import RealDictCursor

from starlette.responses import Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

import uvicorn

from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal

logging.basicConfig(level=logging.DEBUG, filename='app.log', format="%(asctime)s: %(levelname)s: %(message)s")
# log levels: critical; error; warning; info; debug

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal
    try:   
        yield db
    finally:
        db.close_all()

while True:
    try:
        conn = psycopg2.connect(host='localhost', port='5432', database='password_manager', user='postgres', password='postgres', cursor_factory=RealDictCursor)

        cursor = conn.cursor()
        logging.info("Successfully connected to the database.")
        break

    except Exception as error:
        logging.critical("Failed to connect to the database.")
        logging.exception(error)
        time.sleep(2)
        # To-Do: Implement exponential backoff retry mechanism
        continue

PassMan = FastAPI()

class Data (BaseModel):
    platform: str
    username: str
    password: str


@PassMan.get("/")
def default():
    return {"Message": "Server is up and running..."}

@PassMan.get("/apigw")
def apigw():
    return {"Message": "API Gateway is running..."}

@PassMan.get("/test")
def testing_function(db: Session = Depends(get_db)):
    return {"status": "success"}

@PassMan.post("/apigw/accounts", status_code=HTTP_201_CREATED)
def add_account_details(data: Data):

    cursor.execute(""" INSERT INTO account_details (platform_name, username, password) VALUES (%s, %s, %s) RETURNING * """, (data.platform, data.username, data.password))
    conn.commit()

    return {"New Details Added": cursor.fetchone() }

@PassMan.put("/apigw/accounts/{id}")
def update_account_details(id: int, data: Data):

    cursor.execute(""" UPDATE account_details SET platform_name = %s, username = %s, password = %s WHERE id = %s RETURNING * """, (data.platform, data.username, data.password, str(id)))

    updated_data = cursor.fetchone()

    if updated_data == None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")

    conn.commit()

    return {"Details Updated": updated_data}


@PassMan.get("/apigw/accounts")
def get_account_details():

    cursor.execute(""" SELECT * FROM account_details """)
    return { "data": cursor.fetchall() }


@PassMan.get("/apigw/accounts/{id}")
def get_by_id(id: int):

    cursor.execute(""" SELECT * FROM account_details WHERE id = %s""", (str(id),) )
    data = cursor.fetchone()
    
    if not data: 
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")
    
    return { "Requested Data": data }

@PassMan.delete("/apigw/accounts/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_account_data(id: int):
    
    cursor.execute(""" DELETE FROM account_details WHERE id = (%s) RETURNING * """, (str(id),) )
    deleted_data = cursor.fetchone()
    
    if not deleted_data: 
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")


    conn.commit()

    return Response(status_code=HTTP_204_NO_CONTENT)

if __name__ == '__main__':

    uvicorn.run(PassMan, host='0.0.0.0', port=8000, debug=True, reload=False, log_level="info", access_log=True)
    