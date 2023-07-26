from typing import Any, Dict
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import crud
from app.core.config import settings
from app.schemas.user_interaction import UserInteractionCreate, UserInteractionUpdate
from app.schemas.company import CompanyCreate
from app.schemas.branch import BranchCreate
from app.schemas.user import UserCreate
from app.schemas.car import CarCreate
from app.models.car import FuelType, Transmission

from app.tests.utils.car import create_test_cars
from app.tests.utils.company import create_test_companies
from app.tests.utils.branch import create_test_branches
from datetime import datetime
from app.tests.utils.utils import random_email, random_lower_string
from app.tests.utils.company import create_test_companies

def test_create_user_interaction(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Create test company and branch
    company_data = [
        CompanyCreate(name="Company 1")
    ]
    created_company = create_test_companies(db, company_data)
    company_id = created_company[0].id

    branch_data = [
        BranchCreate(branch_name="Branch 1", location="Test location"),
    ]
    created_branches = create_test_branches(db, branch_data, company_id)
    branch_id = created_branches[0].id

    # Create test car
    car_data = [CarCreate(
            make="Test Make 1", model="Test Model 1", year=2022, price=20000.00, kilometers=125000,
            fuel_type=FuelType.DIESEL, transmission=Transmission.AUTOMATIC, color="Red", seats=5
        )]
    created_car = create_test_cars(db=db, car_data=car_data, company_id=company_id, branch_id=branch_id)

    car_id = created_car[0].id

    # create random user
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password, company_id=company_id, branch_id=branch_id)
    user = crud.user.create_with_company_id_and_branch_id(db, obj_in=user_in)
    user_id = user.id

    # Create a new user interaction using the API
    user_interaction_data = {
        "car_id": car_id,
        "user_id": user_id,
        "company_id": company_id,
        "branch_id": branch_id,
        "interaction_type": "Like",
        "timestamp": str(datetime.now())
    }
    created_interaction = make_create_user_interaction_request(client, superuser_token_headers, user_interaction_data)

    # Get the response data (created user interaction) and ensure it matches the input data
    assert created_interaction["user_id"] == user_interaction_data["user_id"]
    assert created_interaction["car_id"] == user_interaction_data["car_id"]
    assert created_interaction["interaction_type"] == user_interaction_data["interaction_type"]

    # Cleanup the test record
    crud.user_interaction.remove(db, id=created_interaction["id"])
    crud.car.remove(db, id=car_id)
    crud.user.remove(db=db, id=user_id)

def test_update_user_interaction(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Create test company and branch
    company_data = [
        CompanyCreate(name="Company 1")
    ]
    created_company = create_test_companies(db, company_data)
    company_id = created_company[0].id

    branch_data = [
        BranchCreate(branch_name="Branch 1", location="Test location"),
    ]
    created_branches = create_test_branches(db, branch_data, company_id)
    branch_id = created_branches[0].id
    # Create test car
    car_data = [CarCreate(
            make="Test Make 1", model="Test Model 1", year=2022, price=20000.00, kilometers=125000,
            fuel_type=FuelType.DIESEL, transmission=Transmission.AUTOMATIC, color="Red", seats=5
        )]
    
    created_car = create_test_cars(db=db, car_data=car_data, company_id=company_id, branch_id=branch_id)

    car_id = created_car[0].id

    # create random user
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password, company_id=company_id, branch_id=branch_id)
    user = crud.user.create_with_company_id_and_branch_id(db, obj_in=user_in)
    user_id = user.id
    # Create a new user interaction using the API
    user_interaction_data = {
        "car_id": car_id,
        "user_id": user_id,
        "company_id": company_id,
        "branch_id": branch_id,
        "interaction_type": "Like",
        "timestamp": str(datetime.now())
    }
    created_interaction = make_create_user_interaction_request(client, superuser_token_headers, user_interaction_data)

    # create random user
    next_user_in = UserCreate(email=random_email(), password=random_lower_string(), company_id=company_id, branch_id=branch_id)
    next_user = crud.user.create_with_company_id_and_branch_id(db, obj_in=next_user_in)
    next_user_id = next_user.id

    # Update the user interaction using the API
    updated_data = {
        "car_id": car_id,
        "user_id": next_user_id,
        "company_id": company_id,
        "branch_id": branch_id,
        "interaction_type": "View",
        "timestamp": str(datetime.now())
    }
    updated_interaction = make_update_user_interaction_request(client, superuser_token_headers, created_interaction["id"], updated_data)

    # Get the response data (updated user interaction) and ensure it matches the updated input data
    assert updated_interaction["user_id"] == updated_data["user_id"]
    assert updated_interaction["interaction_type"] == updated_data["interaction_type"]

    # Cleanup the test record
    crud.user_interaction.remove(db, id=created_interaction["id"])
    crud.car.remove(db, id=car_id)
    crud.user.remove(db=db, id=user_id)
    crud.user.remove(db=db, id=next_user_id)

def test_read_user_interaction(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Create test company and branch
    company_data = [
        CompanyCreate(name="Company 1")
    ]
    created_company = create_test_companies(db, company_data)
    company_id = created_company[0].id

    branch_data = [
        BranchCreate(branch_name="Branch 1", location="Test location"),
    ]
    created_branches = create_test_branches(db, branch_data, company_id)
    branch_id = created_branches[0].id

    # Create test car
    car_data = [CarCreate(
            make="Test Make 1", model="Test Model 1", year=2022, price=20000.00, kilometers=125000,
            fuel_type=FuelType.DIESEL, transmission=Transmission.AUTOMATIC, color="Red", seats=5
        )]
    
    created_car = create_test_cars(db=db, car_data=car_data, company_id=company_id, branch_id=branch_id)

    car_id = created_car[0].id

    # create random user
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password, company_id=company_id, branch_id=branch_id)
    user = crud.user.create_with_company_id_and_branch_id(db, obj_in=user_in)
    user_id = user.id
    # Create a new user interaction using the API
    user_interaction_data = {
        "user_id": user_id,
        "company_id": company_id,
        "branch_id": branch_id,
        "car_id": car_id,
        "interaction_type": "Like",
        "timestamp": str(datetime.now())
    }
    created_interaction = make_create_user_interaction_request(client, superuser_token_headers, user_interaction_data)

    # Make a request to retrieve the created user interaction by ID
    retrieved_interaction = make_get_user_interaction_request(client, superuser_token_headers, created_interaction["id"])

    # Get the response data (retrieved user interaction) and ensure it matches the input data
    assert retrieved_interaction["user_id"] == user_interaction_data["user_id"]
    assert retrieved_interaction["car_id"] == user_interaction_data["car_id"]
    assert retrieved_interaction["interaction_type"] == user_interaction_data["interaction_type"]

    # Cleanup the test record
    crud.user_interaction.remove(db, id=created_interaction["id"])
    crud.car.remove(db, id=car_id)
    crud.user.remove(db=db, id=user_id)

# Add more test cases as needed for other API endpoints

def make_create_user_interaction_request(client: TestClient, superuser_token_headers: Dict[str, str], data: Dict[str, Any]) -> Dict[str, Any]:
    r = client.post(f"{settings.API_V1_STR}/user_interactions/", headers=superuser_token_headers, json=data)
    assert 200 <= r.status_code < 300
    return r.json()

def make_update_user_interaction_request(client: TestClient, superuser_token_headers: Dict[str, str], interaction_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
    r = client.put(f"{settings.API_V1_STR}/user_interactions/{interaction_id}", headers=superuser_token_headers, json=data)
    assert 200 <= r.status_code < 300
    return r.json()

def make_get_user_interaction_request(client: TestClient, superuser_token_headers: Dict[str, str], interaction_id: int) -> Dict[str, Any]:
    r = client.get(f"{settings.API_V1_STR}/user_interactions/{interaction_id}", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    return r.json()
