from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import environment_variable
from app import models
from app.main import PassMan
from app.database import get_db
from app.oauth2 import create_access_token

import pytest

"""
    Testing Database Configuration
"""

SQLALCHEMY_DATABASE_URL = f"postgresql://{environment_variable.DATABASE_USERNAME}:{environment_variable.DATABASE_PASSWORD}@{environment_variable.DATABASE_HOSTNAME}:{environment_variable.DATABASE_PORT}/{environment_variable.TEST_DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_Session():

    #Alembic can also be used to create and destory DB Tables after Test
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:   
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(db_Session):

    def override_get_db():
        try:   
            yield db_Session
        finally:
            db_Session.close()

    PassMan.dependency_overrides[get_db] = override_get_db

    yield TestClient(PassMan)

@pytest.fixture
def test_user(client):
    user_data = {
	"email": "auto_user@mail.com",
	"password": "password"
    }

    res = client.post("/apigw/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"id": test_user['id'], "email": test_user['email']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_add_accounts(test_user, db_Session):
    accounts_data = [{
	"platform": "facebook",
	"username": "user1",
	"password": "password",
    "owner_id": test_user['id']
},{
	"platform": "facebook",
	"username": "user2",
	"password": "password",
    "owner_id": test_user['id']
},{
	"platform": "facebook",
	"username": "user3",
	"password": "password",
    "owner_id": test_user['id']
}]

    def create_account_model(accounts):
        return models.Accounts(**accounts)

    # map(func, data)
    account_map = map(create_account_model, accounts_data)
    accounts = list(account_map)
    
    db_Session.add_all(accounts)
    db_Session.commit()

    accounts_details = db_Session.query(models.Accounts).all()

    return accounts_details