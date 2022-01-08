from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from pydantic.main import Extra
from pydantic.networks import EmailStr

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

class CreateUser(BaseModel, extra=Extra.forbid):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel, extra=Extra.forbid):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class TokenData(BaseModel):
    id: Optional [str] = None
    email: Optional [str] = None
