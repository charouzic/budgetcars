from typing import Any, Dict, List
from app.tests.utils.car import create_test_cars
from app.models.car import FuelType, Transmission
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import crud
from app.core.config import settings
from app.schemas.car import CarCreate, CarUpdate
from app.schemas.company import CompanyCreate
from app.schemas.branch import BranchCreate
from app.tests.utils.company import create_test_companies
from app.tests.utils.branch import create_test_branches


def test_read_cars(
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

    # Create test cars for the company and branch
    car_data = [
        CarCreate(
            make="Test Make 1", model="Test Model 1", year=2022, price=20000.00, kilometers=125000,
            fuel_type=FuelType.DIESEL, transmission=Transmission.AUTOMATIC, color="Red", seats=5
        ),
        CarCreate(
            make="Test Make 2", model="Test Model 2", year=2021, price=18000.00, kilometers=12000, 
            fuel_type=FuelType.PETROL, transmission=Transmission.MANUAL, color="Blue", seats=4
        ),
        CarCreate(
            make="Test Make 3", model="Test Model 3", year=2020, price=15000.00, kilometers=15000,
            fuel_type=FuelType.UNKNOWN, transmission=Transmission.AUTOMATIC, color="Black", seats=5
        ),
    ]
    created_cars = create_test_cars(db=db, car_data=car_data, company_id=company_id, branch_id=branch_id)

    # Make a request to retrieve all cars for the specified company and branch
    r = client.get(f"{settings.API_V1_STR}/company/{company_id}/branch/{branch_id}/cars/", headers=superuser_token_headers)

    # Assert that the request was successful (status code 200-299)
    assert 200 <= r.status_code < 300

    # Get the response data (cars) and ensure the correct number of cars are returned
    cars = r.json()
    assert len(cars) >= len(created_cars)

    # Cleanup the test records
    for car in created_cars:
        crud.car.remove(db, id=car.id)

    crud.branch.remove(db, id=branch_id)
    crud.company.remove(db=db, id=company_id)

def test_create_car(
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

    # Create a new car using the API
    car_data = {
        "make": "Test Make",
        "model": "Test Model",
        "price": 25000.00,
        "year": 2022,
        "kilometers": 125000,
        "fuel_type": "Diesel",
        "transmission": "Automatic",
        "color": "White",
        "seats": 5,
    }
    created_car = make_create_car_request(client, superuser_token_headers, car_data, company_id, created_branches[0].id)

    # Get the response data (created car) and ensure it matches the input data
    assert created_car["make"] == car_data["make"]
    assert created_car["model"] == car_data["model"]
    assert created_car["year"] == car_data["year"]
    assert created_car["price"] == car_data["price"]
    assert created_car["fuel_type"] == car_data["fuel_type"]
    assert created_car["transmission"] == car_data["transmission"]
    assert created_car["color"] == car_data["color"]
    assert created_car["seats"] == car_data["seats"]

    # Cleanup the test record
    crud.car.remove(db, id=created_car["id"])
    crud.branch.remove(db, id=created_branches[0].id)
    crud.company.remove(db=db, id=company_id)

def test_read_car(
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

    # Create a new car for the company and branch
    car_data = {
        "make": "Test Make",
        "model": "Test Model",
        "year": 2022,
        "price": 25000.00,
        "kilometers": 255000,
        "fuel_type": "Petrol",
        "transmission": "Manual",
        "color": "White",
        "seats": 5,
    }
    created_car = make_create_car_request(client, superuser_token_headers, car_data, company_id, created_branches[0].id)

    # Make a request to retrieve the created car by ID
    retrieved_car = make_get_car_request(client, superuser_token_headers, created_car["id"])

    # Get the response data (retrieved car) and ensure it matches the input data
    assert retrieved_car["make"] == car_data["make"]
    assert retrieved_car["model"] == car_data["model"]
    assert retrieved_car["year"] == car_data["year"]
    assert retrieved_car["price"] == car_data["price"]
    assert retrieved_car["fuel_type"] == car_data["fuel_type"]
    assert retrieved_car["transmission"] == car_data["transmission"]
    assert retrieved_car["color"] == car_data["color"]
    assert retrieved_car["seats"] == car_data["seats"]

    # Cleanup the test record
    crud.car.remove(db, id=created_car["id"])
    crud.branch.remove(db, id=created_branches[0].id)
    crud.company.remove(db=db, id=company_id)

# Add more test cases as needed for other API endpoints
def test_read_fuel_types(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/cars/fuel_types/")
    assert r.status_code == 200
    data = r.json()
    assert "fuel_types" in data
    assert len(data["fuel_types"]) > 0

def test_read_transmissions(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/cars/transmissions/")
    assert r.status_code == 200
    data = r.json()
    assert "transmissions" in data
    assert len(data["transmissions"]) > 0

# TODO: add more tests to have 100% test coverage


def make_create_car_request(client: TestClient, superuser_token_headers: Dict[str, str], data: Dict[str, Any], company_id: int, branch_id: int) -> Dict[str, Any]:
    r = client.post(f"{settings.API_V1_STR}/company/{company_id}/branch/{branch_id}/cars/", headers=superuser_token_headers, json=data)
    assert 200 <= r.status_code < 300
    return r.json()

def make_get_car_request(client: TestClient, superuser_token_headers: Dict[str, str], car_id: int) -> Dict[str, Any]:
    r = client.get(f"{settings.API_V1_STR}/car/{car_id}", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    return r.json()
