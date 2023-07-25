from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.company import Company
from app.schemas.company  import CompanyCreate, CompanyUpdate


class CRUDCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    def create_with_name(
        self, db: Session, *, obj_in: CompanyCreate) -> Company:
        db_obj = Company(name=obj_in.name)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Company]:
        return (
            db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )


company = CRUDCompany(Company)
