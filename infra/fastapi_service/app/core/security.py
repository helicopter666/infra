from datetime import UTC, datetime, timedelta
from uuid import uuid4

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


# ── Password ──────────────────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt(rounds=12)).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


# ── JWT ───────────────────────────────────────────────────────────────────────

def _make_token(payload: dict, expire_delta: timedelta) -> str:
    now = datetime.now(UTC)
    data = {
        **payload,
        "jti": str(uuid4()),
        "iat": now,
        "exp": now + expire_delta,
    }
    return jwt.encode(data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_access_token(subject: str, role: str, **extra: object) -> str:
    return _make_token(
        {"sub": subject, "role": role, **extra},
        timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(subject: str) -> str:
    return _make_token(
        {"sub": subject, "type": "refresh"},
        timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
    )


def decode_token(token: str) -> dict:
    """Raises JWTError on invalid/expired token."""
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
