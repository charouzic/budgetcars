from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.schemas.company import CompanyCreate
from app.schemas.branch import BranchCreate
from app.tests.utils.utils import random_email, random_lower_string


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


def test_create_user_existing_username(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    # username = email
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud.user.create(db, obj_in=user_in)
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


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
    # TODO: move this code to utils as a function
    # create a company and branch with given ids
    new_company = CompanyCreate(name="Test Company")
    new_branch = BranchCreate(branch_name="Test Branch", location="Test Location")
    created_company = crud.company.create_with_name(db=db, obj_in=new_company)
    created_branch = crud.branch.create(db=db, obj_in=new_branch, company_id=created_company.id)
    

    users_data = [
        UserCreate(email=random_email(), password=random_lower_string(), company_id=created_company.id, branch_id=created_branch.id),
        UserCreate(email=random_email(), password=random_lower_string(), company_id=created_company.id, branch_id=created_branch.id),
    ]
    new_user_ids = []
    for user_data in users_data:
        new_user = crud.user.create_with_company_id_and_branch_id(db, obj_in=user_data)
        new_user_ids.append(new_user.id)

    # Make a request to retrieve users for the specified company_id
    r = client.get(
        f"{settings.API_V1_STR}/company/{created_company.id}/users/",
        headers=superuser_token_headers,
    )

    # Assert that the request was successful (status code 200-299)
    assert 200 <= r.status_code < 300

    # Get the response data (users) and ensure the correct number of users are returned
    users = r.json()
    assert len(users) == len(users_data)

    for id in new_user_ids:
            crud.user.remove(db, id=id)
    # Cleanup the test records
    crud.branch.remove(db, id=created_branch.id)
    crud.company.remove(db, id=created_company.id)
    
    

def test_read_users_by_company_and_branch(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # TODO: move this code to utils as a function
    # create a company and branch with given ids
    new_company = CompanyCreate(name="Test Company")
    new_branch = BranchCreate(branch_name="Test Branch", location="Test Location")
    created_company = crud.company.create_with_name(db=db, obj_in=new_company)
    created_branch = crud.branch.create(db=db, obj_in=new_branch, company_id=created_company.id)
    
    users_data = [
        UserCreate(email=random_email(), password=random_lower_string(), company_id=created_company.id, branch_id=created_branch.id),
        UserCreate(email=random_email(), password=random_lower_string(), company_id=created_company.id, branch_id=created_branch.id),
    ]

    new_user_ids = []
    for user_data in users_data:
        new_user = crud.user.create_with_company_id_and_branch_id(db, obj_in=user_data)
        new_user_ids.append(new_user.id)

    # Make a request to retrieve users for the specified company_id and branch_id
    r = client.get(
        f"{settings.API_V1_STR}/company/{created_company.id}/branch/{created_branch.id}/users/",
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
    crud.company.remove(db, id=created_company.id)
