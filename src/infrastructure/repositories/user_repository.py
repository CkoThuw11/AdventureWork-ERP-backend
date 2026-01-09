"""User Repository Implementation.

This module contains the concrete implementation of IUserRepository.
"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import User
from src.domain.repositories.user_repository import IUserRepository
from src.infrastructure.database.models import UserModel


class UserRepository(IUserRepository):
    """Concrete implementation of IUserRepository using SQLAlchemy.
    
    This repository handles all database operations for users.
    It maps between ORM models and domain entities.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the user repository.
        
        Args:
            session: The database session.
        """
        self._session = session

    def _to_entity(self, model: UserModel) -> User:
        """Map ORM model to domain entity.
        
        Args:
            model: The UserModel ORM instance.
            
        Returns:
            User domain entity.
        """
        return User(
            id=model.id,
            email=model.email,
            username=model.username,
            full_name=model.full_name,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: User) -> UserModel:
        """Map domain entity to ORM model.
        
        Args:
            entity: The User domain entity.
            
        Returns:
            UserModel ORM instance.
        """
        return UserModel(
            id=entity.id,
            email=entity.email,
            username=entity.username,
            full_name=entity.full_name,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve a user by ID."""
        result = await self._session.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by email address."""
        result = await self._session.execute(select(UserModel).where(UserModel.email == email))
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by username."""
        result = await self._session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """List all users with pagination."""
        result = await self._session.execute(select(UserModel).offset(skip).limit(limit))
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def create(self, user: User) -> User:
        """Create a new user."""
        model = UserModel(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def update(self, user: User) -> User:
        """Update an existing user."""
        result = await self._session.execute(select(UserModel).where(UserModel.id == user.id))
        model = result.scalar_one()

        model.email = user.email
        model.username = user.username
        model.full_name = user.full_name
        model.is_active = user.is_active
        model.updated_at = user.updated_at

        await self._session.commit()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def delete(self, user_id: int) -> bool:
        """Delete a user by ID."""
        result = await self._session.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalar_one_or_none()

        if model:
            await self._session.delete(model)
            await self._session.commit()
            return True
        return False
