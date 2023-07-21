from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.branch import Branch
from app.schemas.branch  import BranchCreate, BranchUpdate


class CRUDBranch(CRUDBase[Branch, BranchCreate, BranchUpdate]):
    def create(
        self, db: Session, *, obj_in: BranchCreate, company_id: int, 
        skip: int = 0, limit: int = 100) -> Branch:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, company_id=company_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Branch]:
        return (
            db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_company(
        self, db: Session, *, company_id: int, skip: int = 0, limit: int = 100
    ) -> List[Branch]:
        return (
            db.query(self.model)
            .filter(Branch.company_id == company_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


branch = CRUDBranch(Branch)
