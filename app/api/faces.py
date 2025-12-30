"""Face API routes."""
import time
import base64
from io import BytesIO
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.face import (
    FaceResponse,
    FaceListResponse,
    FaceSearchResponse,
    FaceSearchResult,
    FaceRegisterRequest,
    FaceListRequest,
    FaceGetRequest,
    FaceDeleteRequest,
    FaceSearchRequest,
    FaceCreate
)
from app.schemas.common import ApiResponse
from app.services.face_service import FaceService
from app.services.application_service import ApplicationService
from app.core.face_engine import get_face_engine
from app.utils.response import success_response, error_response, ErrorCode

router = APIRouter(prefix="/faces", tags=["faces"])

# Get global face engine instance
face_engine = get_face_engine()


@router.post(
    "/register",
    response_model=ApiResponse[FaceResponse],
    summary="Register face"
)
async def register_face(
    request: FaceRegisterRequest,
    db: Session = Depends(get_db)
):
    """Register a new face.
    
    Request body:
    - **app_id**: Application ID (UUID)
    - **person_id**: Person identifier
    - **image_base64**: Base64 encoded face image
    - **metadata**: Optional metadata (JSON object)
    
    Returns:
        统一格式响应，data包含人脸信息
    """
    # Verify application exists
    app = ApplicationService.get_by_id(db, request.app_id)
    if not app:
        return error_response(
            code=ErrorCode.APP_NOT_FOUND,
            message=f"Application with ID '{request.app_id}' not found"
        )
    
    # Decode base64 image
    try:
        image_data = base64.b64decode(request.image_base64)
    except Exception as e:
        return error_response(
            code=ErrorCode.INVALID_BASE64,
            message=f"Invalid base64 image data: {str(e)}"
        )
    
    # Process image: detect face and extract features
    try:
        result = face_engine.process_image(image_data, min_confidence=0.5)
    except Exception as e:
        return error_response(
            code=ErrorCode.INVALID_IMAGE,
            message=f"Failed to process image: {str(e)}"
        )
    
    if result['face_count'] == 0:
        return error_response(
            code=ErrorCode.FACE_NOT_DETECTED,
            message="No face detected in the image"
        )
    
    # Use the extracted feature vector
    feature_vector = result['feature'].tolist()
    
    # Create face record
    try:
        face_data = FaceCreate(
            app_id=request.app_id,
            person_id=request.person_id,
            metadata=request.metadata
        )
        
        face = FaceService.create(
            db=db,
            face_data=face_data,
            feature_vector=feature_vector,
            image_file=BytesIO(image_data),
            filename=f"{request.person_id}.jpg"
        )
        
        return success_response(data=face, message="Face registered successfully")
    except Exception as e:
        return error_response(
            code=ErrorCode.FACE_REGISTER_FAILED,
            message=f"Failed to register face: {str(e)}"
        )


@router.post(
    "/list",
    response_model=ApiResponse[FaceListResponse],
    summary="List faces"
)
def list_faces(
    request: FaceListRequest,
    db: Session = Depends(get_db)
):
    """List faces with pagination.
    
    Request body:
    - **app_id**: Application ID (UUID)
    - **person_id**: Optional person ID filter
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    
    Returns:
        统一格式响应，data包含total和items列表
    """
    # Verify application exists
    app = ApplicationService.get_by_id(db, request.app_id)
    if not app:
        return error_response(
            code=ErrorCode.APP_NOT_FOUND,
            message=f"Application with ID '{request.app_id}' not found"
        )
    
    try:
        if request.person_id:
            faces, total = FaceService.list_by_person(
                db, request.app_id, request.person_id, request.skip, request.limit
            )
        else:
            faces, total = FaceService.list_by_app(
                db, request.app_id, request.skip, request.limit
            )
        
        result = FaceListResponse(total=total, items=faces)
        return success_response(data=result, message="Faces retrieved successfully")
    except Exception as e:
        return error_response(
            code=ErrorCode.INTERNAL_ERROR,
            message=f"Failed to list faces: {str(e)}"
        )


@router.post(
    "/get",
    response_model=ApiResponse[FaceResponse],
    summary="Get face"
)
def get_face(
    request: FaceGetRequest,
    db: Session = Depends(get_db)
):
    """Get a face by ID.
    
    Request body:
    - **face_id**: Face ID (UUID)
    
    Returns:
        统一格式响应，data包含人脸详细信息
    """
    face = FaceService.get_by_id(db, request.face_id)
    if not face:
        return error_response(
            code=ErrorCode.FACE_NOT_FOUND,
            message=f"Face with ID '{request.face_id}' not found"
        )
    return success_response(data=face, message="Face retrieved successfully")


@router.post(
    "/delete",
    response_model=ApiResponse[None],
    summary="Delete face"
)
def delete_face(
    request: FaceDeleteRequest,
    db: Session = Depends(get_db)
):
    """Delete a face (soft delete).
    
    Request body:
    - **face_id**: Face ID (UUID)
    
    Returns:
        统一格式响应，code=0表示删除成功
    """
    success = FaceService.delete(db, request.face_id)
    if not success:
        return error_response(
            code=ErrorCode.FACE_NOT_FOUND,
            message=f"Face with ID '{request.face_id}' not found"
        )
    return success_response(message="Face deleted successfully")


@router.post(
    "/search",
    response_model=ApiResponse[FaceSearchResponse],
    summary="Search faces"
)
async def search_faces(
    request: FaceSearchRequest,
    db: Session = Depends(get_db)
):
    """Search for similar faces.
    
    Request body:
    - **app_id**: Application ID (UUID)
    - **image_base64**: Base64 encoded query face image
    - **top_k**: Number of results to return (1-100, default: 10)
    - **threshold**: Similarity threshold (0.0-1.0, default: 0.6)
    - **metadata_filter**: Optional metadata filter (JSON object)
    
    Returns:
        统一格式响应，data包含搜索结果和查询耗时
    """
    start_time = time.time()
    
    # Verify application exists
    app = ApplicationService.get_by_id(db, request.app_id)
    if not app:
        return error_response(
            code=ErrorCode.APP_NOT_FOUND,
            message=f"Application with ID '{request.app_id}' not found"
        )
    
    # Decode base64 image
    try:
        image_data = base64.b64decode(request.image_base64)
    except Exception as e:
        return error_response(
            code=ErrorCode.INVALID_BASE64,
            message=f"Invalid base64 image data: {str(e)}"
        )
    
    # Use unified face engine for complete search pipeline
    try:
        search_result = face_engine.search_image_in_database(
            db=db,
            image_input=image_data,
            app_id=request.app_id,
            top_k=request.top_k,
            threshold=request.threshold,
            metadata_filter=request.metadata_filter
        )
    except Exception as e:
        return error_response(
            code=ErrorCode.FACE_SEARCH_FAILED,
            message=f"Failed to search faces: {str(e)}"
        )
    
    if not search_result['face_detected']:
        return error_response(
            code=ErrorCode.FACE_NOT_DETECTED,
            message="No face detected in the image"
        )
    
    # Convert results to response format
    results = [
        FaceSearchResult(
            face_id=match['face_id'],
            person_id=match['person_id'],
            similarity=match['similarity'],
            image_url=match['image_url'],
            metadata=match.get('metadata')
        )
        for match in search_result['matches']
    ]
    
    response_data = FaceSearchResponse(
        query_time_ms=search_result['query_time_ms'],
        results=results
    )
    
    return success_response(data=response_data, message="Face search completed successfully")
