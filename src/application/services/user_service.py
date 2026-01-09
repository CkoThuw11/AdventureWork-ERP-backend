"""User Service.

This module contains the User service implementing user-related use cases.
"""

from datetime import datetime

from src.application.dtos.user_dto import CreateUserCommand, UpdateUserCommand, UserDto
from src.domain.entities.user import User
from src.domain.exceptions import (
    DomainValidationError,
    EntityAlreadyExistsError,
    EntityNotFoundError,
)
from src.domain.repositories.user_repository import IUserRepository


class UserService:
    """User service implementing user-related business logic.

    This service orchestrates user operations by coordinating
    between the domain layer and repository implementations.
    """

    def __init__(self, user_repository: IUserRepository) -> None:
        """Initialize the user service.

        Args:
            user_repository: The user repository implementation.
        """
        self._user_repo = user_repository

    async def create_user(self, command: CreateUserCommand) -> UserDto:
        """Create a new user.

        Args:
            command: The create user command with validated input.

        Returns:
            UserDto containing the created user data.

        Raises:
            DomainValidationError: If the command is invalid.
            EntityAlreadyExistsError: If a user with the email or username exists.
        """
        if not command.is_valid():
            raise DomainValidationError("Invalid user creation command")

        # Check if user already exists
        existing_user = await self._user_repo.get_by_email(command.email)
        if existing_user:
            raise EntityAlreadyExistsError("User", command.email)

        existing_user = await self._user_repo.get_by_username(command.username)
        if existing_user:
            raise EntityAlreadyExistsError("User", command.username)

        # Create domain entity
        now = datetime.utcnow()
        user = User(
            id=None,
            email=command.email,
            username=command.username,
            full_name=command.full_name,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        # Persist via repository
        created_user = await self._user_repo.create(user)

        # Map to DTO
        return UserDto.model_validate(created_user)

    async def get_user_by_id(self, user_id: int) -> UserDto:
        """Retrieve a user by ID.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            UserDto containing the user data.

        Raises:
            EntityNotFoundError: If the user is not found.
        """
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise EntityNotFoundError("User", user_id)

        return UserDto.model_validate(user)

    async def list_users(self, skip: int = 0, limit: int = 100) -> list[UserDto]:
        """List all users with pagination.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List of UserDto objects.
        """
        users = await self._user_repo.list_all(skip=skip, limit=limit)
        return [UserDto.model_validate(user) for user in users]

    async def update_user(self, user_id: int, command: UpdateUserCommand) -> UserDto:
        """Update an existing user.

        Args:
            user_id: The unique identifier of the user.
            command: The update user command with validated input.

        Returns:
            UserDto containing the updated user data.

        Raises:
            EntityNotFoundError: If the user is not found.
        """
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise EntityNotFoundError("User", user_id)

        # Update domain entity
        if command.full_name:
            user.update_profile(command.full_name)

        # Persist changes
        updated_user = await self._user_repo.update(user)

        return UserDto.model_validate(updated_user)

    async def deactivate_user(self, user_id: int) -> UserDto:
        """Deactivate a user account.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            UserDto containing the deactivated user data.

        Raises:
            EntityNotFoundError: If the user is not found.
        """
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise EntityNotFoundError("User", user_id)

        # Apply business logic
        user.deactivate()

        # Persist changes
        updated_user = await self._user_repo.update(user)

        return UserDto.model_validate(updated_user)
