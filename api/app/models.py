import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from .database import Base


class Clan(Base):
    """
    SQLAlchemy ORM model for the clans table.
    
    Attributes:
        id: Unique UUID identifier (auto-generated)
        name: Clan name (required)
        region: Region code (e.g., "TR", "US")
        created_at: UTC timestamp of when the clan was created (auto-generated)
    """
    __tablename__ = "clans"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    name = Column(String(255), nullable=False, index=True)
    region = Column(String(10), nullable=False, index=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    
    def __repr__(self):
        return f"<Clan(id={self.id}, name='{self.name}', region='{self.region}')>"
