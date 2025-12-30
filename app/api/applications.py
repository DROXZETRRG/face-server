"""Application API routes."""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    ApplicationListResponse,
    ApplicationListRequest,
    ApplicationGetRequest,
    ApplicationUpdateRequest,
    ApplicationDeleteRequest
)
from app.schemas.common import ApiResponse
from app.services.application_service import ApplicationService
from app.utils.response import success_response, error_response, ErrorCode

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post(
    "/create",
    response_model=ApiResponse[ApplicationResponse],
    summary="Create application"
)
def create_application(
    app_data: ApplicationCreate,
    db: Session = Depends(get_db)
):
    """Create a new application.
    
    Request body:
    - **app_code**: Application code (unique identifier)
    - **app_name**: Application name
    
    Returns:
        统一格式响应，code=0表示成功，data包含应用信息
    """
    # Check if app_code already exists
    existing = ApplicationService.get_by_code(db, app_data.app_code)
    if existing:
        return error_response(
            code=ErrorCode.APP_CODE_EXISTS,
            message=f"Application with code '{app_data.app_code}' already exists"
        )
    
    try:
        app = ApplicationService.create(db, app_data)
        return success_response(data=app, message="Application created successfully")
    except Exception as e:
        return error_response(
            code=ErrorCode.APP_CREATE_FAILED,
            message=f"Failed to create application: {str(e)}"
        )


@router.post(
    "/list",
    response_model=ApiResponse[ApplicationListResponse],
    summary="List applications"
)
def list_applications(
    request: ApplicationListRequest,
    db: Session = Depends(get_db)
):
    """List all applications with pagination.
    
    Request body:
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    
    Returns:
        统一格式响应，data包含total和items列表
    """
    try:
        apps, total = ApplicationService.list_all(db, request.skip, request.limit)
        result = ApplicationListResponse(total=total, items=apps)
        return success_response(data=result, message="Applications retrieved successfully")
    except Exception as e:
        return error_response(
            code=ErrorCode.INTERNAL_ERROR,
            message=f"Failed to list applications: {str(e)}"
        )


@router.post(
    "/get",
    response_model=ApiResponse[ApplicationResponse],
    summary="Get application"
)
def get_application(
    request: ApplicationGetRequest,
    db: Session = Depends(get_db)
):
    """Get an application by ID.
    
    Request body:
    - **app_id**: Application ID (UUID)
    
    Returns:
        统一格式响应，data包含应用详细信息
    """
    app = ApplicationService.get_by_id(db, request.app_id)
    if not app:
        return error_response(
            code=ErrorCode.APP_NOT_FOUND,
            message=f"Application with ID '{request.app_id}' not found"
        )
    return success_response(data=app, message="Application retrieved successfully")


@router.post(
    "/update",
    response_model=ApiResponse[ApplicationResponse],
    summary="Update application"
)
def update_application(
    request: ApplicationUpdateRequest,
    db: Session = Depends(get_db)
):
    """Update an application.
    
    Request body:
    - **app_id**: Application ID (UUID)
    - **app_name**: New application name (optional)
    
    Returns:
        统一格式响应，data包含更新后的应用信息
    """
    app = ApplicationService.update(db, request.app_id, request)
    if not app:
        return error_response(
            code=ErrorCode.APP_NOT_FOUND,
            message=f"Application with ID '{request.app_id}' not found"
        )
    return success_response(data=app, message="Application updated successfully")


@router.post(
    "/delete",
    response_model=ApiResponse[None],
    summary="Delete application"
)
def delete_application(
    request: ApplicationDeleteRequest,
    db: Session = Depends(get_db)
):
    """Delete an application (soft delete).
    
    Request body:
    - **app_id**: Application ID (UUID)
    
    Returns:
        统一格式响应，code=0表示删除成功
    """
    success = ApplicationService.delete(db, request.app_id)
    if not success:
        return error_response(
            code=ErrorCode.APP_NOT_FOUND,
            message=f"Application with ID '{request.app_id}' not found"
        )
    return success_response(message="Application deleted successfully")
