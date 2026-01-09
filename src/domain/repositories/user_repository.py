"""User Repository Interface.

This module defines the abstract interface for user data access.
"""

from abc import ABC, abstractmethod

from src.domain.entities.user import User


class IUserRepository(ABC):
    """Abstract interface for User repository.

    This interface defines the contract for user data access operations.
    Implementations must be provided in the Infrastructure layer.
    """

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        """Retrieve a user by ID.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            User entity if found, None otherwise.
        """
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by email address.

        Args:
            email: The email address of the user.

        Returns:
            User entity if found, None otherwise.
        """
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        """Retrieve a user by username.

        Args:
            username: The username of the user.

        Returns:
            User entity if found, None otherwise.
        """
        pass

    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        """List all users with pagination.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List of User entities.
        """
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user.

        Args:
            user: The user entity to create.

        Returns:
            The created user entity with generated ID.
        """
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """Update an existing user.

        Args:
            user: The user entity with updated data.

        Returns:
            The updated user entity.
        """
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        """Delete a user by ID.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            True if deleted successfully, False otherwise.
        """
        pass
