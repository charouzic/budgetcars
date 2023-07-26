from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.schemas.company import CompanyCreate
from app.schemas.branch import BranchCreate
from app.tests.utils.utils import random_email, random_lower_string
from app.tests.utils.company import create_test_companies

def test_get_users_superuser_me(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER


def test_create_user_new_email(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_email(db, email=username)
    assert user
    assert user.email == created_user["email"]

    crud.user.remove(db=db, id=created_user["id"])


def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    user_id = user.id
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}", headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.user.get_by_email(db, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]
    crud.user.remove(db, id=user_id)


def test_create_user_existing_username(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    # username = email
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    my_user = crud.user.create(db, obj_in=user_in)
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user
    crud.user.remove(db=db, id=my_user.id)

def test_create_user_by_normal_user(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=normal_user_token_headers, json=data,
    )
    assert r.status_code == 400


def test_retrieve_users(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud.user.create(db, obj_in=user_in)

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    crud.user.create(db, obj_in=user_in2)

    r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users) > 1
    for item in all_users:
        assert "email" in item

def test_read_users_by_company(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Create test companies and a branch
    test_companies_data = [
        CompanyCreate(name="Test Company 1"),
        CompanyCreate(name="Test Company 2"),
    ]
    created_companies = create_test_companies(db, test_companies_data)

    new_branch = BranchCreate(branch_name="Test Branch", location="Test Location")
    created_branch = crud.branch.create(db=db, obj_in=new_branch, company_id=created_companies[0].id)

    users_data = [
        UserCreate(email=random_email(), password=random_lower_string(), company_id=created_companies[0].id, branch_id=created_branch.id),
        UserCreate(email=random_email(), password=random_lower_string(), company_id=created_companies[0].id, branch_id=created_branch.id),
    ]
    new_user_ids = []
    for user_data in users_data:
        new_user = crud.user.create_with_company_id_and_branch_id(db, obj_in=user_data)
        new_user_ids.append(new_user.id)

    # Make a request to retrieve users for the specified company_id
    r = client.get(
        f"{settings.API_V1_STR}/company/{created_companies[0].id}/users/",
        headers=superuser_token_headers,
    )

    # Assert that the request was successful (status code 200-299)
    assert 200 <= r.status_code < 300

    # Get the response data (users) and ensure the correct number of users are returned
    users = r.json()
    assert len(users) == len(users_data)

    # Cleanup the test records
    for id in new_user_ids:
            crud.user.remove(db, id=id)
    crud.branch.remove(db, id=created_branch.id)

    # Cleanup the test companies and branch
    for company in created_companies:
        crud.company.remove(db, id=company.id)
    
    

def test_read_users_by_company_and_branch(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Create test companies and a branch
    test_companies_data = [
        CompanyCreate(name="Test Company 1"),
        CompanyCreate(name="Test Company 2"),
    ]
    created_companies = create_test_companies(db, test_companies_data)

    new_branch = BranchCreate(branch_name="Test Branch", location="Test Location")
    created_branch = crud.branch.create(db=db, obj_in=new_branch, company_id=created_companies[0].id)

    users_data = [
        UserCreate(email=random_email(), password=random_lower_string(), company_id=created_companies[0].id, branch_id=created_branch.id),
        UserCreate(email=random_email(), password=random_lower_string(), company_id=created_companies[0].id, branch_id=created_branch.id),
    ]

    new_user_ids = []
    for user_data in users_data:
        new_user = crud.user.create_with_company_id_and_branch_id(db, obj_in=user_data)
        new_user_ids.append(new_user.id)

    # Make a request to retrieve users for the specified company_id and branch_id
    r = client.get(
        f"{settings.API_V1_STR}/company/{created_companies[0].id}/branch/{created_branch.id}/users/",
        headers=superuser_token_headers,
    )

    # Assert that the request was successful (status code 200-299)
    assert 200 <= r.status_code < 300

    # Get the response data (users) and ensure the correct number of users are returned
    users = r.json()
    assert len(users) == len(users_data)

    # Cleanup the test records
    for id in new_user_ids:
            crud.user.remove(db, id=id)
   
    crud.branch.remove(db, id=created_branch.id)

    # Cleanup the test companies
    for company in created_companies:
        crud.company.remove(db, id=company.id)

def test_update_user_me(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Create a test user with known email
    user_email = random_email()
    user_password = "testpassword"
    user_in = UserCreate(email=user_email, password=user_password)
    created_user = crud.user.create(db, obj_in=user_in)

    # Login the user to get an access token
    login_data = {
        "username": user_email,
        "password": user_password,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 200
    access_token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Make a request to update the user's data
    new_full_name = "New Full Name"
    new_email = random_email()
    r = client.put(
        f"{settings.API_V1_STR}/users/me",
        headers=headers,
        json={"full_name": new_full_name, "email": new_email, "password":user_password},
    )
    assert r.status_code == 200

    # Get the updated user data
    updated_user = r.json()
    assert updated_user["full_name"] == new_full_name
    assert updated_user["email"] == new_email

    # Cleanup the test user
    crud.user.remove(db, id=created_user.id)


def test_read_user_by_id(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Create a test user with known email
    user_email = random_email()
    user_password = "testpassword"
    user_in = UserCreate(email=user_email, password=user_password)
    created_user = crud.user.create(db, obj_in=user_in)

    # Make a request to get the user by ID
    user_id = created_user.id
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}", headers=superuser_token_headers
    )
    assert r.status_code == 200

    # Get the response data (user) and ensure it matches the test user
    user = r.json()
    assert user["id"] == created_user.id
    assert user["email"] == created_user.email

    # Cleanup the test user
    crud.user.remove(db, id=created_user.id)


def test_create_user_open(
    client: TestClient, db: Session
) -> None:
    # Enable open user registration for this test
    settings.USERS_OPEN_REGISTRATION = True

    # Make a request to create a new user without being logged in
    new_email = random_email()
    new_password = random_lower_string()
    new_full_name = "New User"
    r = client.post(
        f"{settings.API_V1_STR}/users/open",
        json={
            "email": new_email,
            "password": new_password,
            "full_name": new_full_name,
        },
    )
    assert r.status_code == 200

    # Get the response data (created user) and ensure it matches the input data
    created_user = r.json()
    assert created_user["email"] == new_email
    assert created_user["full_name"] == new_full_name

    # Make sure the user is actually created in the database
    db_user = crud.user.get_by_email(db, email=new_email)
    assert db_user is not None
    assert db_user.email == new_email
    assert db_user.full_name == new_full_name

    # Cleanup the test user
    crud.user.remove(db, id=db_user.id)

    # Disable open user registration after the test
    settings.USERS_OPEN_REGISTRATION = False


def test_update_user(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Create a test user with known email
    user_email = random_email()
    user_password = "testpassword"
    user_in = UserCreate(email=user_email, password=user_password)
    created_user = crud.user.create(db, obj_in=user_in)

    # Make a request to update the user's data
    new_full_name = "Updated User"
    new_email = random_email()
    r = client.put(
        f"{settings.API_V1_STR}/users/{created_user.id}",
        headers=superuser_token_headers,
        json={"full_name": new_full_name, "email": new_email, "password": user_password},
    )
    assert r.status_code == 200

    # Get the updated user data
    updated_user = r.json()
    assert updated_user["full_name"] == new_full_name
    assert updated_user["email"] == new_email

    # Cleanup the test user
    crud.user.remove(db, id=created_user.id)


# The following test case covers the case when the user is not a superuser.
# This case ensures that a non-superuser is not allowed to retrieve a specific user by ID.
def test_read_user_by_id_not_superuser(
    client: TestClient, normal_user_token_headers: Dict[str, str], db: Session
) -> None:
    # Create a test user with known email
    user_email = random_email()
    user_password = "testpassword"
    user_in = UserCreate(email=user_email, password=user_password)
    created_user = crud.user.create(db, obj_in=user_in)

    # Make a request to get the user by ID using normal user credentials (not a superuser)
    user_id = created_user.id
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}", headers=normal_user_token_headers
    )
    assert r.status_code == 400  # The non-superuser should not have enough privileges

    # Cleanup the test user
    crud.user.remove(db, id=created_user.id)


def test_update_user_me_not_superuser(
    client: TestClient, normal_user_token_headers: Dict[str, str], db: Session
) -> None:
    # Create a test user with known email
    user_email = random_email()
    user_password = "testpassword"
    user_in = UserCreate(email=user_email, password=user_password)
    created_user = crud.user.create(db, obj_in=user_in)

    # Make a request to update the user's data using normal user credentials (not a superuser)
    new_full_name = "Updated User"
    new_email = random_email()
    r = client.put(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers,
        json={"full_name": new_full_name, "email": new_email, "password": user_password},
    )
    assert r.status_code == 200

    # Get the updated user data
    updated_user = r.json()
    assert updated_user["full_name"] == new_full_name
    assert updated_user["email"] == new_email

    # Cleanup the test user
    crud.user.remove(db, id=created_user.id)