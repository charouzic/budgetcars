from typing import TYPE_CHECKING

from enum import Enum

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Enum as EnumSA
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class InteractionType(str, Enum):
    VIEW = "View"
    LIKE = "Like"

if TYPE_CHECKING:
    from .branch import Branch  # noqa: F401
    from .company import Company  # noqa: F401
    from .car import Car  # noqa: F401
    from .user import User  # noqa: F401


class UserInteraction(Base):
    __tablename__ = "user_interactions"
    id = Column(Integer, primary_key=True, index=True)
    # Relationships with Company and Branch
    # for now company_id and branch_id can be null
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False)

    interaction_type = Column(EnumSA(InteractionType), index=True, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    car = relationship("Car", back_populates="interactions")
    user = relationship("User", back_populates="interactions")
    company = relationship("Company", back_populates="interactions")
    branch = relationship("Branch", back_populates="interactions")
    
