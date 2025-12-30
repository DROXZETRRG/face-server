"""Face schemas."""
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field


class FaceBase(BaseModel):
    """Base face schema."""
    person_id: str = Field(..., min_length=1, max_length=100, description="Person ID")
    metadata: Optional[Dict[str, Any]] = Field(None, alias="face_metadata", description="Additional metadata")


class FaceCreate(FaceBase):
    """Schema for creating a face."""
    app_id: UUID = Field(..., description="Application ID")
    # Note: image will be uploaded as file, feature_vector will be extracted


class FaceRegisterRequest(BaseModel):
    """Schema for registering a face."""
    app_id: UUID = Field(..., description="Application ID")
    person_id: str = Field(..., min_length=1, max_length=100, description="Person ID")
    image_base64: str = Field(..., description="Base64 encoded image")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class FaceListRequest(BaseModel):
    """Schema for listing faces."""
    app_id: UUID = Field(..., description="Application ID")
    person_id: Optional[str] = Field(None, description="Optional person ID filter")
    skip: int = Field(0, ge=0, description="Number of records to skip")
    limit: int = Field(100, ge=1, le=1000, description="Maximum number of records to return")


class FaceGetRequest(BaseModel):
    """Schema for getting a face."""
    face_id: UUID = Field(..., description="Face ID")


class FaceDeleteRequest(BaseModel):
    """Schema for deleting a face."""
    face_id: UUID = Field(..., description="Face ID")


class FaceResponse(FaceBase):
    """Schema for face response."""
    id: UUID
    app_id: UUID
    image_url: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True


class FaceListResponse(BaseModel):
    """Schema for listing faces."""
    total: int
    items: List[FaceResponse]


class FaceSearchRequest(BaseModel):
    """Schema for face search request."""
    app_id: UUID = Field(..., description="Application ID")
    image_base64: str = Field(..., description="Base64 encoded query image")
    top_k: int = Field(10, ge=1, le=100, description="Number of results to return")
    threshold: float = Field(0.6, ge=0.0, le=1.0, description="Similarity threshold")
    metadata_filter: Optional[Dict[str, Any]] = Field(None, description="Metadata filter")


class FaceSearchResult(BaseModel):
    """Schema for a single search result."""
    face_id: UUID
    person_id: str
    similarity: float
    image_url: str
    metadata: Optional[Dict[str, Any]]


class FaceSearchResponse(BaseModel):
    """Schema for face search response."""
    query_time_ms: float
    results: List[FaceSearchResult]
