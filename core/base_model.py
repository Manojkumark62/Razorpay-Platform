from sqlalchemy import Column, Boolean, DateTime
from datetime import datetime, timezone
from core.base import Base


def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class BaseModel(Base):
    __abstract__ = True

    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)