from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .branch import Branch  # noqa: F401


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    # Relationship with branches
    branches = relationship("Branch", back_populates="companies")
    # Relationship with cars
    cars = relationship("Car", back_populates="branches")