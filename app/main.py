from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from random import randrange
import time, logging

import psycopg2
from psycopg2.extras import RealDictCursor

from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

logging.basicConfig(level=logging.DEBUG, filename='app.log', format="%(asctime)s: %(levelname)s: %(message)s")
# log levels: critical; error; warning; info; debug

while True:
    try:
        conn = psycopg2.connect(host='localhost', port='5432', database='password_manager', user='db_user', password='password', cursor_factory=RealDictCursor)

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

dataArray = [
    {"platform": "facebook", "username": "User1", "password": "pass@123", "id": 1},
    {"platform": "instagram", "username": "User2", "password": "pass@123", "id": 2},
    {"platform": "snapchat", "username": "User3", "password": "pass@123", "id": 3}
]

def find_data_in_array(id):
    for details in dataArray:
        if details["id"] == id:
            return details

def find_index(id):
    for i, p in enumerate(dataArray):
        if p["id"] == id:
            return i


class Data (BaseModel):
    platform: str
    username: str
    password: str


@PassMan.get("/")
def default():
    return {"Message": "Server is up and running..."}

@PassMan.get("/apigw")
def default():
    return {"Message": "API Gateway is running..."}

@PassMan.post("/apigw/accounts", status_code=HTTP_201_CREATED)
def add_account_details(data: Data):
    data_dict = data.dict()
    data_dict['id'] = randrange(0, 1000)
    dataArray.append(data_dict)
    return {"New Details Added": data_dict}

@PassMan.put("/apigw/accounts/{id}")
def update_account_details(id: int, data: Data):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")
    
    updated_data = data.dict()
    updated_data['id'] = id
    dataArray[index] = updated_data
    return {"Details Updated": updated_data}


@PassMan.get("/apigw/accounts")
def get_account_details():
    return { "data": dataArray }

@PassMan.get("/apigw/accounts/{id}")
def get_by_id(id: int):
    data = find_data_in_array(id)
    if not data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")
    return {"Requested Data": data}

@PassMan.delete("/apigw/accounts/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_account_data(id: int):
    deleted_data = find_data_in_array(id)
    if not deleted_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} doesn't exist")
    dataArray.remove(deleted_data)
    return {"Deleted Successfully": deleted_data}

