from typing import Optional

from pydantic import BaseModel


# Shared properties
class CompanyBase(BaseModel):
    name: Optional[str] = None


# Properties to receive on company creation
class CompanyCreate(CompanyBase):
    pass


# Properties to receive on company update
class CompanyUpdate(CompanyBase):
    pass


# Properties shared by models stored in DB
class CompanyInDBBase(CompanyBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Company(CompanyInDBBase):
    pass


# Properties properties stored in DB
class CompanyInDB(CompanyInDBBase):
    pass
