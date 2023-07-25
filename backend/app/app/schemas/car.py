from typing import Optional
from app.models.car import FuelType, Transmission
# from app.schemas.fuel_type import FuelType
# from app.schemas.transmission import Transmission

from pydantic import BaseModel


# Shared properties
class CarBase(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    price: Optional[float] = None
    year: Optional[int] = None
    kilometers: Optional[int] = None
    fuel_type: Optional[FuelType] = None  # Use FuelType enum type
    transmission: Optional[Transmission] = None  # Use Transmission enum type
    color: Optional[str] = None
    seats: Optional[int] = None


# Properties to receive on car creation
class CarCreate(CarBase):
    make: str
    model: str
    price: float
    year: int
    kilometers: int
    fuel_type: FuelType
    transmission: Transmission
    color: str
    seats: int


# Properties to receive on car update
class CarUpdate(CarBase):
    pass


# Properties shared by models stored in DB
class CarInDBBase(CarBase):
    id: int
    make: str
    model: str
    price: float
    year: int
    kilometers: int
    fuel_type: FuelType
    transmission: Transmission
    color: str
    seats: int

    class Config:
        orm_mode = True


# Properties to return to client
class Car(CarInDBBase):
    CarInDBBase


# Properties properties stored in DB
class CarInDB(CarInDBBase):
    pass
