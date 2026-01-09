"""User ORM Model.

This module defines the SQLAlchemy ORM model for the users table.
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.connection import Base


class UserModel(Base):
    """SQLAlchemy ORM model for users table.
    
    This model maps to the database table and should NOT be exposed
    outside the Infrastructure layer. Always map to domain entities.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        """String representation of the user model."""
        return f"<UserModel(id={self.id}, username={self.username}, email={self.email})>"
