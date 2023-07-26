from typing import Any, Dict, List
from app.tests.utils.branch import create_test_branches
from app.tests.utils.company import create_test_companies
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import crud
from app.core.config import settings
from app.schemas.branch import BranchCreate, BranchUpdate
from app.schemas.company import CompanyCreate

def test_read_branches(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Create test company
    company_data = [
        CompanyCreate(name="Company 1")
    ]
    created_company = create_test_companies(db, company_data)
    company_id = created_company[0].id

    branch_data = [
        BranchCreate(branch_name="Branch 1", location="Test location"),
        BranchCreate(branch_name="Branch 2", location="Test location"),
        BranchCreate(branch_name="Branch 3", location="Test location"),
    ]
    created_branches = create_test_branches(db, branch_data, company_id)

    # Make a request to retrieve all branches for the specified company
    r = client.get(f"{settings.API_V1_STR}/branches/", headers=superuser_token_headers)

    # Assert that the request was successful (status code 200-299)
    assert 200 <= r.status_code < 300

    # Get the response data (branches) and ensure the correct number of branches are returned
    branches = r.json()
    assert len(branches) >= len(created_branches)

    # Cleanup the test records
    for branch in created_branches:
        crud.branch.remove(db, id=branch.id)
    crud.company.remove(db=db, id=company_id)

def test_create_branch(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Create a new branch using the API
    # Create test company
    company_data = [
        CompanyCreate(name="Company 1")
    ]
    created_company = create_test_companies(db, company_data)
    company_id = created_company[0].id

    branch_name = "Test Branch"
    data = {"branch_name": branch_name, "company_id": company_id, "location": "Test Location"}
    created_branch = make_create_branch_request(client, superuser_token_headers, data, company_id)

    # Get the response data (created branch) and ensure it matches the input data
    assert created_branch["branch_name"] == branch_name
    assert created_branch["company_id"] == company_id

    # Cleanup the test record
    crud.branch.remove(db, id=created_branch["id"])
    crud.company.remove(db=db, id=company_id)

def test_update_branch(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Create a new branch for a specific company (replace company_id with the desired company ID)
    # Create test company
    company_data = [
        CompanyCreate(name="Company 1")
    ]
    created_company = create_test_companies(db, company_data)
    company_id = created_company[0].id

    new_branch = BranchCreate(branch_name="Test Branch", company_id=company_id, location="Test loc")
    created_branch = crud.branch.create(db, obj_in=new_branch, company_id=company_id)

    # Update the branch using the API
    updated_branch_name = "Updated Branch Name"
    data = {"branch_name": updated_branch_name}
    updated_branch = make_update_branch_request(client, superuser_token_headers, created_branch.id, data)

    # Get the response data (updated branch) and ensure it matches the input data
    assert updated_branch["branch_name"] == updated_branch_name

    # Cleanup the test record
    crud.branch.remove(db, id=created_branch.id)
    crud.company.remove(db=db, id=company_id)

def test_read_branch(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Create a new branch for a specific company (replace company_id with the desired company ID)
    # Create test company
    company_data = [
        CompanyCreate(name="Company 1")
    ]
    created_company = create_test_companies(db, company_data)
    company_id = created_company[0].id

    new_branch = BranchCreate(branch_name="Test Branch", company_id=company_id, location = "Test location")
    created_branch = crud.branch.create(db, obj_in=new_branch, company_id=company_id)

    # Make a request to retrieve the created branch by ID
    retrieved_branch = make_get_branch_request(client, superuser_token_headers, created_branch.id)

    # Get the response data (retrieved branch) and ensure it matches the input data
    assert retrieved_branch["branch_name"] == new_branch.branch_name
    assert retrieved_branch["company_id"] == company_id

    # Cleanup the test record
    crud.branch.remove(db, id=created_branch.id)
    crud.company.remove(db=db, id=company_id)

def test_delete_branch(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Create a new branch for a specific company (replace company_id with the desired company ID)
    # Create test company
    company_data = [
        CompanyCreate(name="Company 1")
    ]
    created_company = create_test_companies(db, company_data)
    company_id = created_company[0].id

    new_branch = BranchCreate(branch_name="Test Branch", company_id=company_id, location = "Test location")
    created_branch = crud.branch.create(db, obj_in=new_branch, company_id=company_id)

    # Make a request to delete the created branch by ID
    deleted_branch = make_delete_branch_request(client, superuser_token_headers, created_branch.id)

    # Get the response data (deleted branch) and ensure it matches the input data
    assert deleted_branch["branch_name"] == new_branch.branch_name
    assert deleted_branch["company_id"] == company_id

    # Verify that the branch record was deleted from the database
    assert crud.branch.get(db, id=created_branch.id) is None
    crud.company.remove(db=db, id=company_id)

def test_update_branch_not_found(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Make a request to update a branch that does not exist (ID: 999)
    branch_id = 999
    updated_branch_data = {"branch_name": "Updated Branch Name"}

    r = client.put(
        f"{settings.API_V1_STR}/branches/{branch_id}",
        headers=superuser_token_headers,
        json=updated_branch_data,
    )

    # Assert that the request returns a 404 Not Found status code
    assert r.status_code == 404

def test_read_branch_not_found(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Make a request to get a branch that does not exist (ID: 999)
    branch_id = 999

    r = client.get(
        f"{settings.API_V1_STR}/branches/{branch_id}",
        headers=superuser_token_headers,
    )

    # Assert that the request returns a 404 Not Found status code
    assert r.status_code == 404

def test_delete_branch_not_found(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Make a request to delete a branch that does not exist (ID: 999)
    branch_id = 999

    r = client.delete(
        f"{settings.API_V1_STR}/branches/{branch_id}",
        headers=superuser_token_headers,
    )

    # Assert that the request returns a 404 Not Found status code
    assert r.status_code == 404

def test_create_branch_with_invalid_data(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Create test company
    company_data = [
        CompanyCreate(name="Company 1")
    ]
    created_company = create_test_companies(db, company_data)
    company_id = created_company[0].id

    # Attempt to create a new branch with missing data (branch_name is missing)
    invalid_branch_data = {"company_id": company_id, "location": "Test Location"}

    # Make a request to create the branch with invalid data
    r = client.post(
        f"{settings.API_V1_STR}/companies/{company_id}/branches/",
        headers=superuser_token_headers,
        json=invalid_branch_data,
    )

    # Assert that the request returns a 422 Unprocessable Entity status code
    assert r.status_code == 422

    # Cleanup the test record
    crud.company.remove(db=db, id=company_id)

def test_create_branch_with_invalid_company_id(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # Attempt to create a new branch with an invalid company_id (ID: 999)
    invalid_company_id = 999
    branch_data = {"branch_name": "Test Branch", "company_id": invalid_company_id, "location": "Test Location"}

    # Make a request to create the branch with an invalid company_id
    r = client.post(
        f"{settings.API_V1_STR}/companies/{invalid_company_id}/branches/",
        headers=superuser_token_headers,
        json=branch_data,
    )

    # Assert that the request returns a 404 Not Found status code
    assert r.status_code == 404



def make_create_branch_request(client: TestClient, superuser_token_headers: Dict[str, str], data: Dict[str, Any], company_id: int) -> Dict[str, Any]:
    r = client.post(f"{settings.API_V1_STR}/companies/{company_id}/branches/", headers=superuser_token_headers, json=data)
    assert 200 <= r.status_code < 300
    return r.json()

def make_update_branch_request(client: TestClient, superuser_token_headers: Dict[str, str], branch_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
    r = client.put(f"{settings.API_V1_STR}/branches/{branch_id}", headers=superuser_token_headers, json=data)
    assert 200 <= r.status_code < 300
    return r.json()

def make_get_branch_request(client: TestClient, superuser_token_headers: Dict[str, str], branch_id: int) -> Dict[str, Any]:
    r = client.get(f"{settings.API_V1_STR}/branches/{branch_id}", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    return r.json()

def make_delete_branch_request(client: TestClient, superuser_token_headers: Dict[str, str], branch_id: int) -> Dict[str, Any]:
    r = client.delete(f"{settings.API_V1_STR}/branches/{branch_id}", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    return r.json()
