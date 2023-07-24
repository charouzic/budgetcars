from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .company import Company  # noqa: F401
    from .user import User  # noqa: F401
    from .user_interaction import UserInteraction  # noqa: F401

class Branch(Base):
    __tablename__ = "branches"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    branch_name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    # Relationships
    company = relationship("Company", back_populates="branches")
    cars = relationship("Car", back_populates="branch")
    users = relationship("User", back_populates="branch")
    interactions = relationship("UserInteraction", back_populates="branch")
