from typing import Any, Dict
from app.tests.utils.company import create_test_companies
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import crud
from app.core.config import settings
from app.schemas.company import CompanyCreate

def test_read_companies(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Create test companies
    company_data = [
        CompanyCreate(name="Company 1"),
        CompanyCreate(name="Company 2"),
        CompanyCreate(name="Company 3"),
    ]
    created_companies = create_test_companies(db, company_data)

    # Make a request to retrieve all companies
    r = client.get(f"{settings.API_V1_STR}/companies/", headers=superuser_token_headers)

    # Assert that the request was successful (status code 200-299)
    assert 200 <= r.status_code < 300

    # Get the response data (companies) and ensure the correct number of companies are returned
    companies = r.json()
    assert len(companies) >= len(created_companies)

    # Cleanup the test records
    for company in created_companies:
        crud.company.remove(db, id=company.id)

def test_create_company(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Create a new company using the API
    company_name = "Test Company"
    data = {"name": company_name}
    created_company = make_create_company_request(client, superuser_token_headers, data)

    # Get the response data (created company) and ensure it matches the input data
    assert created_company["name"] == company_name

    # Cleanup the test record
    crud.company.remove(db, id=created_company["id"])

def test_update_company(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Create a new company
    company_name = "Test Company"
    new_company = CompanyCreate(name=company_name)
    created_company = crud.company.create_with_name(db, obj_in=new_company)

    # Update the company using the API
    updated_company_name = "Updated Company Name"
    data = {"name": updated_company_name}
    updated_company = make_update_company_request(client, superuser_token_headers, created_company.id, data)

    # Get the response data (updated company) and ensure it matches the input data
    assert updated_company["name"] == updated_company_name

    # Cleanup the test record
    crud.company.remove(db, id=created_company.id)

def test_read_company(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Create a new company
    company_name = "Test Company"
    new_company = CompanyCreate(name=company_name)
    created_company = crud.company.create_with_name(db, obj_in=new_company)

    # Make a request to retrieve the created company by ID
    retrieved_company = make_get_company_request(client, superuser_token_headers, created_company.id)

    # Get the response data (retrieved company) and ensure it matches the input data
    assert retrieved_company["name"] == company_name

    # Cleanup the test record
    crud.company.remove(db, id=created_company.id)

def test_delete_company(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Create a new company
    company_name = "Test Company"
    new_company = CompanyCreate(name=company_name)
    created_company = crud.company.create_with_name(db, obj_in=new_company)

    # Make a request to delete the created company by ID
    deleted_company = make_delete_company_request(client, superuser_token_headers, created_company.id)

    # Get the response data (deleted company) and ensure it matches the input data
    assert deleted_company["name"] == company_name

    # Verify that the company record was deleted from the database
    assert crud.company.get(db, id=created_company.id) is None

def test_update_company_not_found(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Make a request to update a company that does not exist (ID: 999)
    company_id = 999
    updated_company_data = {"name": "Updated Company Name"}

    r = client.put(
        f"{settings.API_V1_STR}/companies/{company_id}",
        headers=superuser_token_headers,
        json=updated_company_data,
    )

    # Assert that the request returns a 404 Not Found status code
    assert r.status_code == 404

def test_read_company_not_found(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Make a request to get a company that does not exist (ID: 999)
    company_id = 999

    r = client.get(
        f"{settings.API_V1_STR}/companies/{company_id}",
        headers=superuser_token_headers,
    )

    # Assert that the request returns a 404 Not Found status code
    assert r.status_code == 404

def test_delete_company_not_found(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Make a request to delete a company that does not exist (ID: 999)
    company_id = 999

    r = client.delete(
        f"{settings.API_V1_STR}/companies/{company_id}",
        headers=superuser_token_headers,
    )

    # Assert that the request returns a 404 Not Found status code
    assert r.status_code == 404

def make_create_company_request(client: TestClient, superuser_token_headers: Dict[str, str], data: Dict[str, Any]) -> Dict[str, Any]:
    r = client.post(f"{settings.API_V1_STR}/companies/", headers=superuser_token_headers, json=data)
    assert 200 <= r.status_code < 300
    return r.json()

def make_update_company_request(client: TestClient, superuser_token_headers: Dict[str, str], company_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
    r = client.put(f"{settings.API_V1_STR}/companies/{company_id}", headers=superuser_token_headers, json=data)
    assert 200 <= r.status_code < 300
    return r.json()

def make_get_company_request(client: TestClient, superuser_token_headers: Dict[str, str], company_id: int) -> Dict[str, Any]:
    r = client.get(f"{settings.API_V1_STR}/companies/{company_id}", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    return r.json()

def make_delete_company_request(client: TestClient, superuser_token_headers: Dict[str, str], company_id: int) -> Dict[str, Any]:
    r = client.delete(f"{settings.API_V1_STR}/companies/{company_id}", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    return r.json()