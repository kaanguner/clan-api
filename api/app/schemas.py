from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, field_validator


class ClanBase(BaseModel):
    """Base schema for clan data."""
    name: str = Field(..., min_length=1, max_length=255, description="Clan name")
    region: str = Field(..., min_length=2, max_length=10, description="Region code (e.g., TR, US)")
    
    @field_validator('region')
    @classmethod
    def region_uppercase(cls, v: str) -> str:
        """Ensure region code is uppercase."""
        return v.upper()


class ClanCreate(ClanBase):
    """Schema for creating a new clan."""
    pass


class ClanResponse(ClanBase):
    """Schema for clan response with all fields."""
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class ClanListResponse(BaseModel):
    """Schema for listing multiple clans."""
    clans: List[ClanResponse]
    count: int


class ClanSearchRequest(BaseModel):
    """Schema for clan search parameters."""
    name: str = Field(..., min_length=3, description="Search term (minimum 3 characters)")


class MessageResponse(BaseModel):
    """Schema for simple message responses."""
    message: str
    id: Optional[UUID] = None
