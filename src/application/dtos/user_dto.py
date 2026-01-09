"""User DTOs.

This module defines all Data Transfer Objects for User operations.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateUserCommand(BaseModel):
    """Command for creating a new user.

    This DTO validates input for user creation.
    """

    model_config = ConfigDict(strict=True)

    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    full_name: str = Field(..., min_length=1, max_length=100, description="User full name")

    def is_valid(self) -> bool:
        """Validate the command.

        Returns:
            True if the command is valid.
        """
        return len(self.username) >= 3 and len(self.full_name) >= 1


class UpdateUserCommand(BaseModel):
    """Command for updating an existing user."""

    model_config = ConfigDict(strict=True)

    full_name: str | None = Field(
        None, min_length=1, max_length=100, description="Updated full name"
    )


class UserDto(BaseModel):
    """User response DTO.

    This DTO is used to return user data to the client.
    It maps from the User domain entity.
    """

    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int = Field(..., description="User unique identifier")
    email: str = Field(..., description="User email address")
    username: str = Field(..., description="Username")
    full_name: str = Field(..., description="User full name")
    is_active: bool = Field(..., description="Whether the user account is active")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class UserListDto(BaseModel):
    """DTO for paginated user list response."""

    model_config = ConfigDict(strict=True)

    users: list[UserDto] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    skip: int = Field(..., description="Number of records skipped")
    limit: int = Field(..., description="Maximum number of records returned")
