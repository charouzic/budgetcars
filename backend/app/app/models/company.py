from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .branch import Branch  # noqa: F401
    from .user import User  # noqa: F401
    from .user_interaction import UserInteraction  # noqa: F401

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    # Relationships
    branches = relationship("Branch", back_populates="company")
    cars = relationship("Car", back_populates="companies")
    users = relationship("User", back_populates="company")
    interactions = relationship("UserInteraction", back_populates="company")