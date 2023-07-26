from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app import crud
from app.schemas.company import CompanyCreate

def create_test_companies(db: Session, companies: List[CompanyCreate]) -> List[Dict[str, Any]]:
    """
    Create test companies in the database using the provided data.

    Parameters:
        db (Session): The SQLAlchemy database session.
        companies (List[CompanyCreate]): A list of CompanyCreate objects containing company data.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing the created companies.
    """
    created_companies = []
    for company in companies:
        created_company = crud.company.create_with_name(db, obj_in=company)
        created_companies.append(created_company)
    return created_companies

# Usage example:
# test_data = [
#     CompanyCreate(name="Company 1"),
#     CompanyCreate(name="Company 2"),
#     CompanyCreate(name="Company 3"),
# ]
# created_companies = create_test_companies(db, test_data)