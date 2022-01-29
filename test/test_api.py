from app import schemas
from app.config import environment_variable

from jose import jwt

import pytest

# unit test to check if server is running or not
def test_default(client):
     
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Server is up and running..."}

# Integration test for create new user functionality
def test_create_user(client):

    res = client.post("/apigw/users/", json={
	"email": "test_user@mail.com",
	"password": "password"
    })

    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "test_user@mail.com"

# login functionality test
# 'test_user': pytest fixture is used to create a new user first, then run the test for login functionality
def test_login_user(client, test_user):

    res = client.post("/apigw/login/", data={
	"username": test_user['email'],
	"password": test_user['password']
    })

    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token, environment_variable.SECRET_KEY, algorithms=[environment_variable.ALGORITHM])

    id = payload.get("id")
    email = payload.get("email")

    # check for expected value after successful login
    assert id == test_user['id']
    assert email == test_user['email']
    assert res.status_code == 200
    assert login_res.token_type == "bearer"

# multiple test cases
@pytest.mark.parametrize("email, password, status_code", [
    ('auto_user@mail.com', 'wrongpw', 403),
    ('wrong@mail.com', 'password', 403),
    ('wrong@mail.com', 'wrongpw', 403),
    (None, 'password', 422),
    ('auto_user@mail.com', None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/apigw/login/", data={
	"username": email,
	"password": password
    })

    assert res.status_code == status_code
    #assert res.json().get('detail') == "Invalid Credentails"

def test_get_all_account(authorized_client, test_add_accounts):
    
    res = authorized_client.get("/apigw/accounts/")
    assert res.status_code == 200
    assert len(res.json()) == len(test_add_accounts)