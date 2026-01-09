"""User Entity.

This module defines the User domain entity.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """User domain entity.

    Represents a user in the system with core business attributes.
    This is a pure domain object with no infrastructure dependencies.
    """

    id: int | None
    email: str
    username: str
    full_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    def deactivate(self) -> None:
        """Deactivate the user account.

        Business rule: A user can be deactivated but not deleted.
        """
        self.is_active = False

    def activate(self) -> None:
        """Activate the user account."""
        self.is_active = True

    def update_profile(self, full_name: str) -> None:
        """Update user profile information.

        Args:
            full_name: The new full name for the user.
        """
        self.full_name = full_name
        self.updated_at = datetime.utcnow()
