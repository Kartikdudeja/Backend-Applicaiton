from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import redis

from .config import environment_variable

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database-name>"

SQLALCHEMY_DATABASE_URL = f"postgresql://{environment_variable.DATABASE_USERNAME}:{environment_variable.DATABASE_PASSWORD}@{environment_variable.DATABASE_HOSTNAME}:{environment_variable.DATABASE_PORT}/{environment_variable.DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:   
        yield db
    finally:
        db.close()

redis_client = redis.Redis(host=environment_variable.REDIS_HOSTNAME, port=environment_variable.REDIS_PORT, db=environment_variable.REDIS_DATABASE)