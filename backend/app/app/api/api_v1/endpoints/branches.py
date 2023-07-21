from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/branches/", response_model=List[schemas.Branch])
def read_branches(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve branches.
    """
    branches = crud.branch.get_multi(db, skip=skip, limit=limit)
    return branches


@router.post("/companies/{company_id}/branches/", response_model=schemas.Branch)
def create_branch(
    *,
    company_id: int = Path(..., title="The ID of the company to which the branch belongs", ge=1),
    branch_in: schemas.BranchCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Create a new branch record for a specific company.
    """
    # Check if the company with the given company_id exists in the database
    company = crud.company.get(db=db, id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Create the branch and associate it with the company
    branch = crud.branch.create(db=db, obj_in=branch_in, company_id=company_id)
    return branch


@router.put("/branches/{branch_id}", response_model=schemas.Branch)
def update_branch(
    *,
    branch_id: int = Path(..., title="The ID of the branch to update", ge=1),
    branch_in: schemas.BranchUpdate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Update a branch.
    """
    # Check if the branch with the given branch_id exists in the database
    branch = crud.branch.get(db=db, id=branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    # Update the branch with the provided data
    branch = crud.branch.update(db=db, db_obj=branch, obj_in=branch_in)
    return branch


@router.get("/branches/{branch_id}", response_model=schemas.Branch)
def read_branch(
    *,
    branch_id: int = Path(..., title="The ID of the branch to retrieve", ge=1),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get branch by ID.
    """
    # Check if the branch with the given branch_id exists in the database
    branch = crud.branch.get(db=db, id=branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    return branch


@router.delete("/branches/{branch_id}", response_model=schemas.Branch)
def delete_branch(
    *,
    branch_id: int = Path(..., title="The ID of the branch to delete", ge=1),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Delete a branch record.
    """
    # Check if the branch with the given branch_id exists in the database
    branch = crud.branch.get(db=db, id=branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    # Delete the branch
    deleted_branch = crud.branch.remove(db=db, id=branch_id)
    return deleted_branch
