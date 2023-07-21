from typing import TYPE_CHECKING

from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Enum as EnumSA
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .branch import Branch  # noqa: F401
    from .company import Company # noqa: F401

class FuelType(str, Enum):
    PETROL = "Petrol"
    DIESEL = "Diesel"
    UNKNOWN = "Unknown"

class Transmission(str, Enum):
    MANUAL = "Manual"
    AUTOMATIC = "Automatic"
    UNKNOWN = "Unknown"

class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False)
    make = Column(String, index=True, nullable=False)
    model = Column(String, index=True, nullable=False)
    price = Column(Float, index=True, nullable=False)
    year = Column(Integer, index=True, nullable=False)
    kilometers = Column(Integer, index=True, nullable=False)

    # Use EnumSA to define fuel_type and transmission as enums
    fuel_type = Column(EnumSA(FuelType), index=True, nullable=False)
    transmission = Column(EnumSA(Transmission), index=True, nullable=False)

    color = Column(String, index=True, nullable=False)
    seats = Column(Integer, index=True, nullable=False)

    # Relationship with branch
    branch = relationship("Branch", back_populates="cars")
    # Relationship with company
    companies = relationship("Company", back_populates="cars")