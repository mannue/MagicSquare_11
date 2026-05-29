"""Tests for the User entity."""

import pytest

from src.entity.models.user import User


def test_user_creation_sets_fields() -> None:
    """User 생성 시 필드가 올바르게 설정된다."""
    # Arrange
    user_id = 1
    name = "Alice"
    email = "alice@example.com"

    # Act
    user = User(user_id=user_id, name=name, email=email)

    # Assert
    assert user.user_id == user_id
    assert user.name == name
    assert user.email == email
    assert user.is_active is True


def test_user_creation_with_invalid_email_raises_value_error() -> None:
    """유효하지 않은 이메일이면 ValueError가 발생한다."""
    # Arrange
    invalid_email = "invalid-email"

    # Act / Assert
    with pytest.raises(ValueError):
        User(user_id=1, name="Alice", email=invalid_email)


def test_rename_with_blank_name_raises_value_error() -> None:
    """빈 이름으로 변경하면 ValueError가 발생한다."""
    # Arrange
    user = User(user_id=1, name="Alice", email="alice@example.com")

    # Act / Assert
    with pytest.raises(ValueError):
        user.rename("   ")


def test_deactivate_sets_user_inactive() -> None:
    """deactivate 호출 시 사용자가 비활성화된다."""
    # Arrange
    user = User(user_id=1, name="Alice", email="alice@example.com")

    # Act
    user.deactivate()

    # Assert
    assert user.is_active is False
