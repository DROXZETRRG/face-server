"""Application schemas."""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class ApplicationBase(BaseModel):
    """Base application schema."""
    app_code: str = Field(..., min_length=1, max_length=100, description="Application code")
    app_name: str = Field(..., min_length=1, max_length=200, description="Application name")


class ApplicationCreate(ApplicationBase):
    """Schema for creating an application."""
    pass


class ApplicationUpdate(BaseModel):
    """Schema for updating an application."""
    app_name: Optional[str] = Field(None, min_length=1, max_length=200, description="Application name")


class ApplicationResponse(ApplicationBase):
    """Schema for application response."""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ApplicationListRequest(BaseModel):
    """Schema for listing applications."""
    skip: int = Field(0, ge=0, description="Number of records to skip")
    limit: int = Field(100, ge=1, le=1000, description="Maximum number of records to return")


class ApplicationGetRequest(BaseModel):
    """Schema for getting an application."""
    app_id: UUID = Field(..., description="Application ID")


class ApplicationUpdateRequest(ApplicationUpdate):
    """Schema for updating an application."""
    app_id: UUID = Field(..., description="Application ID")


class ApplicationDeleteRequest(BaseModel):
    """Schema for deleting an application."""
    app_id: UUID = Field(..., description="Application ID")


class ApplicationListResponse(BaseModel):
    """Schema for listing applications."""
    total: int
    items: list[ApplicationResponse]
