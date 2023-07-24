from typing import Optional

from datetime import datetime

from pydantic import BaseModel

from app.models.user_interaction import InteractionType

# Shared properties
class UserInteractionBase(BaseModel):
    car_id: int
    user_id: int
    company_id: Optional[int] = None
    branch_id: Optional[int] = None
    interaction_type: InteractionType
    timestamp: datetime

# Properties to receive via API on creation
class UserInteractionCreate(UserInteractionBase):
    pass

# Properties to receive via API on update
class UserInteractionUpdate(UserInteractionBase):
    pass

# Properties shared by models stored in DB
class UserInteractionInDBBase(UserInteractionBase):
    id: int

    class Config:
        orm_mode = True

# Properties to return to client
class UserInteraction(UserInteractionInDBBase):
    pass


# Properties properties stored in DB
class UserInteractionInDB(UserInteractionInDBBase):
    pass
