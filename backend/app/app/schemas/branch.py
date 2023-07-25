from typing import Optional

from pydantic import BaseModel


# Shared properties
class BranchBase(BaseModel):
    branch_name: Optional[str] = None
    location: Optional[str] = None


# Properties to receive on branch creation
class BranchCreate(BranchBase):
    branch_name: str
    location: str


# Properties to receive on branch update
class BranchUpdate(BranchBase):
    pass


# Properties shared by models stored in DB
class BranchInDBBase(BranchBase):
    id: int
    branch_name: str
    location: str
    company_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Branch(BranchInDBBase):
    pass


# Properties properties stored in DB
class BranchInDB(BranchInDBBase):
    pass
