# All details related to database connection

import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import redis
import logging

from app.config import environment_variable

logger = logging.getLogger(__name__)

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database-name>"

SQLALCHEMY_DATABASE_URL = f"postgresql://{environment_variable.DATABASE_USERNAME}:{environment_variable.DATABASE_PASSWORD}@{environment_variable.DATABASE_HOSTNAME}:{environment_variable.DATABASE_PORT}/{environment_variable.DATABASE_NAME}"

# database engine to create db tables
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#session for db call
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# create a session for every db call
def get_db():
    db = SessionLocal()
    try:   
        yield db
    finally:
        db.close()

# Redis Connection
redis_client = redis.Redis(host=environment_variable.REDIS_HOSTNAME, port=environment_variable.REDIS_PORT, db=environment_variable.REDIS_DATABASE)

# Retry mechanism for connecting with Redis DB
# To-Do: Try to implement a Exponential Back-Off Algorithm
# while True:

#     try:

#         redis_client = redis.Redis(host=environment_variable.REDIS_HOSTNAME, port=environment_variable.REDIS_PORT, db=environment_variable.REDIS_DATABASE)
#         logger.info("Successfully Connected to Redis")
#         break

#     except:
#         logger.error("Failed to connect to Redis. Retrying in 3 seconds...")
#         time.sleep(3)
#         continue
