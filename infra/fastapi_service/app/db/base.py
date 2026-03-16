from sqlalchemy.orm import DeclarativeBase, MappedColumn, mapped_column
from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""
    pass


class TimestampMixin:
    """Миксин: автоматические created_at / updated_at."""
    created_at: MappedColumn[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: MappedColumn[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
        onupdate=func.now(), nullable=False
    )


class UUIDPrimaryKeyMixin:
    """Миксин: UUID первичный ключ."""
    id: MappedColumn[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
