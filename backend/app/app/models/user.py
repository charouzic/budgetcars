from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .branch import Branch  # noqa: F401
    from .company import Company  # noqa: F401
    from .user_interaction import UserInteraction  # noqa: F401


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    # Relationships with Company and Branch
    # for now company_id and branch_id can be null
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=True)

    company = relationship("Company", back_populates="users")
    branch = relationship("Branch", back_populates="users")
    interactions = relationship("UserInteraction", back_populates="user")
