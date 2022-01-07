from datetime import datetime
from pydantic import BaseModel
from pydantic.main import Extra

class AccoutData (BaseModel):
    platform: str
    username: str
    password: str

    class Config:
        orm_mode = True
        extra = Extra.forbid 

class CreateAccount (AccoutData):
    pass

class UpdateAccount (BaseModel, extra=Extra.forbid):
    password: str

class AccountResponse (BaseModel):
    id: int
    platform: str
    username: str
    created_at: datetime
    
    class Config:
        orm_mode = True
