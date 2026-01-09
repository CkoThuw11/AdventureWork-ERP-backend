"""Dependency Injection Configuration.

This module defines dependency injection for services and repositories.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.user_service import UserService
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.user_repository import UserRepository


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> UserRepository:
    """Get user repository instance.

    Args:
        session: Database session from dependency.

    Returns:
        UserRepository instance.
    """
    return UserRepository(session)


def get_user_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    """Get user service instance.

    Args:
        user_repo: User repository from dependency.

    Returns:
        UserService instance.
    """
    return UserService(user_repo)
