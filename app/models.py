# Defines Tables Defination 

from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

from app.database import Base

class Accounts(Base):
    __tablename__ = "account_details"

    # 'account_details' table stores information regarding credentials saved by user

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    platform = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="NO ACTION"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # defines relationship b/w 'account_details' and 'users' table
    owner = relationship("Users")

class Users(Base):
    __tablename__ = "users"

    # 'users' table store the information about Users

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    