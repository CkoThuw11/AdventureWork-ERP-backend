"""User API Routes.

This module defines all user-related API endpoints.
Routers are responsible ONLY for parsing requests and returning responses.
All business logic is delegated to the UserService.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_user_service
from src.application.dtos.user_dto import CreateUserCommand, UpdateUserCommand, UserDto
from src.application.services.user_service import UserService
from src.domain.exceptions import (
    DomainValidationError,
    EntityAlreadyExistsError,
    EntityNotFoundError,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    response_model=UserDto,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
async def create_user(
    command: CreateUserCommand,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserDto:
    """Create a new user.

    Args:
        command: User creation command with validated data.
        user_service: Injected user service.

    Returns:
        Created user data.

    Raises:
        HTTPException: If validation fails or user already exists.
    """
    try:
        return await user_service.create_user(command)
    except DomainValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message) from e
    except EntityAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message) from e


@router.get(
    "/{user_id}",
    response_model=UserDto,
    summary="Get user by ID",
)
async def get_user(
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserDto:
    """Get a user by ID.

    Args:
        user_id: The unique identifier of the user.
        user_service: Injected user service.

    Returns:
        User data.

    Raises:
        HTTPException: If user is not found.
    """
    try:
        return await user_service.get_user_by_id(user_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e


@router.get(
    "/",
    response_model=list[UserDto],
    summary="List all users",
)
async def list_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
    skip: int = 0,
    limit: int = 100,
) -> list[UserDto]:
    """List all users with pagination.

    Args:
        skip: Number of records to skip.
        limit: Maximum number of records to return.
        user_service: Injected user service.

    Returns:
        List of users.
    """
    return await user_service.list_users(skip=skip, limit=limit)


@router.patch(
    "/{user_id}",
    response_model=UserDto,
    summary="Update user",
)
async def update_user(
    user_id: int,
    command: UpdateUserCommand,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserDto:
    """Update a user.

    Args:
        user_id: The unique identifier of the user.
        command: User update command with validated data.
        user_service: Injected user service.

    Returns:
        Updated user data.

    Raises:
        HTTPException: If user is not found.
    """
    try:
        return await user_service.update_user(user_id, command)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e


@router.post(
    "/{user_id}/deactivate",
    response_model=UserDto,
    summary="Deactivate user",
)
async def deactivate_user(
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserDto:
    """Deactivate a user account.

    Args:
        user_id: The unique identifier of the user.
        user_service: Injected user service.

    Returns:
        Deactivated user data.

    Raises:
        HTTPException: If user is not found.
    """
    try:
        return await user_service.deactivate_user(user_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
