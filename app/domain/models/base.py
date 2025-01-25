from __future__ import annotations

import datetime
import uuid
from typing import TypeVar

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.settings.config import config

BaseDbModelT = TypeVar('BaseDbModelT', bound='BaseDbModel')


engine: AsyncEngine = create_async_engine(url=str(config.database_dsn), pool_size=20)
SessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False
)


class TimestampedDbModelMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True, server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )


class BaseDbModel(DeclarativeBase):
    pk: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, server_default=func.gen_random_uuid())


class TimestampedDbModel(BaseDbModel, TimestampedDbModelMixin):
    __abstract__ = True
