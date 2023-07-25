from fastapi import HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from app import crud, models, schemas

def validate_user_interaction(db: Session, user_interaction_in: schemas.UserInteractionCreate):
    if user_interaction_in.company_id:
        get_existing_company(db, user_interaction_in.company_id)
    if user_interaction_in.branch_id:
        get_existing_branch(db, user_interaction_in.branch_id, company_id=user_interaction_in.company_id)
    if user_interaction_in.car_id:
        get_existing_car(db, user_interaction_in.car_id, branch_id=user_interaction_in.branch_id, company_id=user_interaction_in.company_id)
    if user_interaction_in.user_id:
        get_existing_user(db, user_interaction_in.user_id, branch_id=user_interaction_in.branch_id, company_id=user_interaction_in.company_id)

def get_existing_branch(db: Session, branch_id: int, company_id: Optional[int] = None):
    branch = crud.branch.get(db=db, id=branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    # If company_id is provided, check if the branch belongs to the specified company
    if company_id and branch.company_id != company_id:
        raise HTTPException(status_code=400, detail="Branch does not belong to the specified company")
    return branch

def get_existing_company(db: Session, company_id: int):
    company = crud.company.get(db=db, id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

def get_existing_car(db: Session, car_id: int, branch_id: Optional[int] = None, company_id: Optional[int] = None):
    car = crud.car.get(db=db, id=car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    # If branch_id is provided, check if the car belongs to the specified branch
    if branch_id and car.branch_id != branch_id:
        raise HTTPException(status_code=400, detail="Car does not belong to the specified branch")
    # If company_id is provided, check if the car belongs to the specified company
    if company_id and car.company_id != company_id:
        raise HTTPException(status_code=400, detail="Car does not belong to the specified company")
    return car

def get_existing_user(db: Session, user_id: int, branch_id: Optional[int] = None, company_id: Optional[int] = None):
    user = crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # If branch_id is provided, check if the user belongs to the specified branch
    if branch_id and user.branch_id != branch_id:
        raise HTTPException(status_code=400, detail="User does not belong to the specified branch")
    # If company_id is provided, check if the user belongs to the specified company
    if company_id and user.company_id != company_id:
        raise HTTPException(status_code=400, detail="User does not belong to the specified company")
    return user