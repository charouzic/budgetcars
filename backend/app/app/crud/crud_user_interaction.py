import random
from typing import List, Optional, Type, TypeVar
from app.core.filtering_utils import content_filtering

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user_interaction import UserInteraction, InteractionType
from app.schemas.user_interaction import UserInteractionCreate, UserInteractionUpdate

class CRUDUserInteraction(CRUDBase[UserInteraction, UserInteractionCreate, UserInteractionUpdate]):  
    def get_multi_by_company_and_branch(
            self, db: Session, *, company_id: int, branch_id: int, skip: int = 0, limit: int = 100
    ) -> List[UserInteraction]:
        return db.query(self.model).filter(
            self.model.company_id == company_id,
            self.model.branch_id == branch_id).offset(skip).limit(limit).all()
    
    def get_multi_by_car(self, db: Session, *, car_id: int, skip: int = 0, limit: int = 100
    ) -> List[UserInteraction]:
        return db.query(self.model).filter(
            self.model.car_id == car_id).offset(skip).limit(limit).all()
    
    def get_multi_by_user(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[UserInteraction]:
        return db.query(self.model).filter(
            self.model.user_id == user_id).offset(skip).limit(limit).all()
    
user_interaction = CRUDUserInteraction(UserInteraction)