from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/password_manager"
# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database-name>"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:   
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', port='5432', database='password_manager', user='postgres', password='postgres', cursor_factory=RealDictCursor)

#         cursor = conn.cursor()
#         logging.info("Successfully connected to the database.")
#         break

#     except Exception as error:
#         logging.critical("Failed to connect to the database.")
#         logging.exception(error)
#         time.sleep(2)
#         # To-Do: Implement exponential backoff retry mechanism
#         continue
