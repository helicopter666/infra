import pytest
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
    )


@pytest.fixture
def admin_user(db) -> User:
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="adminpass123",
    )


@pytest.fixture
def auth_client(api_client, user) -> APIClient:
    """APIClient с JWT-аутентификацией обычного пользователя."""
    from jose import jwt
    from django.conf import settings
    from datetime import datetime, timedelta, UTC
    from uuid import uuid4

    token = jwt.encode(
        {
            "sub": str(user.pk),
            "jti": str(uuid4()),
            "role": "user",
            "exp": datetime.now(UTC) + timedelta(minutes=15),
            "iat": datetime.now(UTC),
        },
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user) -> APIClient:
    """APIClient с JWT-аутентификацией администратора."""
    from jose import jwt
    from django.conf import settings
    from datetime import datetime, timedelta, UTC
    from uuid import uuid4

    token = jwt.encode(
        {
            "sub": str(admin_user.pk),
            "jti": str(uuid4()),
            "role": "admin",
            "exp": datetime.now(UTC) + timedelta(minutes=15),
            "iat": datetime.now(UTC),
        },
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client
