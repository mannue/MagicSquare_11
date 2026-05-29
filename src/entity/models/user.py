"""User entity for domain rules and state transitions."""

from dataclasses import dataclass


@dataclass
class User:
    """Represents a user in the domain layer.

    Attributes:
        user_id: Unique identifier of the user.
        name: Display name of the user.
        email: Email address used for contact and identity.
        is_active: Whether the user is active.
    """

    user_id: int
    name: str
    email: str
    is_active: bool = True

    def __post_init__(self) -> None:
        """Validate initial user state."""
        self._validate_name(self.name)
        self._validate_email(self.email)

    def rename(self, new_name: str) -> None:
        """Update the user's display name.

        Args:
            new_name: New display name.

        Raises:
            ValueError: If the name is blank.
        """
        self._validate_name(new_name)
        self.name = new_name

    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False

    def activate(self) -> None:
        """Activate the user account."""
        self.is_active = True

    @staticmethod
    def _validate_name(name: str) -> None:
        """Validate user name.

        Args:
            name: User name to validate.

        Raises:
            ValueError: If name is blank.
        """
        if not name.strip():
            raise ValueError("name must not be blank")

    @staticmethod
    def _validate_email(email: str) -> None:
        """Validate email format with a simple domain check.

        Args:
            email: Email string to validate.

        Raises:
            ValueError: If email format is invalid.
        """
        if "@" not in email or email.startswith("@") or email.endswith("@"):
            raise ValueError("email format is invalid")
