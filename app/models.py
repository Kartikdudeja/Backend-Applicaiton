from sqlalchemy import Column, Integer, String
from .database import Base

class Accounts(Base):
    __tablename__ = "account_details"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    platform_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    #created_at =