"""Domain Exceptions.

This module defines all domain-specific exceptions.
These exceptions represent business rule violations and domain errors.
"""


class DomainException(Exception):
    """Base exception for all domain errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class DomainValidationError(DomainException):
    """Raised when domain validation fails."""

    pass


class EntityNotFoundError(DomainException):
    """Raised when an entity is not found."""

    def __init__(self, entity_name: str, entity_id: str | int) -> None:
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(f"{entity_name} with id {entity_id} not found")


class EntityAlreadyExistsError(DomainException):
    """Raised when attempting to create an entity that already exists."""

    def __init__(self, entity_name: str, identifier: str) -> None:
        self.entity_name = entity_name
        self.identifier = identifier
        super().__init__(f"{entity_name} with identifier {identifier} already exists")


class BusinessRuleViolationError(DomainException):
    """Raised when a business rule is violated."""

    pass
