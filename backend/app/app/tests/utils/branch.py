from typing import List
from sqlalchemy.orm import Session
from app import crud
from app.schemas.branch import BranchCreate
from app.models.branch import Branch

def create_test_branches(db: Session, branch_data: List[BranchCreate], company_id: int) -> List[Branch]:
    created_branches = []
    for branch_in in branch_data:
        branch = crud.branch.create(db=db, obj_in=branch_in, company_id=company_id)
        created_branches.append(branch)
    return created_branches