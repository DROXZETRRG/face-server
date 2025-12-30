"""WebSocket API for real-time face detection."""
import base64
import json
from io import BytesIO
from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
import numpy as np
from PIL import Image

from app.database import SessionLocal
from app.core.face_engine import get_face_engine
from app.models.face import Face

router = APIRouter()

# Get global face engine instance
face_engine = get_face_engine()


@router.websocket("/ws/detect")
async def websocket_detect(
    websocket: WebSocket,
    app_id: str = Query(..., description="Application ID"),
    threshold: float = Query(0.6, description="Similarity threshold")
):
    """WebSocket endpoint for real-time face detection.
    
    Query Parameters:
    - app_id: Application ID (UUID)
    - threshold: Similarity threshold (0.0-1.0)
    
    Message Format (Client -> Server):
    - Binary mode (recommended): Send JPEG/PNG binary data directly
    - JSON mode (fallback):
    ```json
    {
        "image": "base64_encoded_image",
        "threshold": 0.6  // Optional, override query param
    }
    ```
    
    Response Format (Server -> Client):
    ```json
    {
        "face_count": 2,
        "faces": [
            {
                "bbox": [x1, y1, x2, y2],
                "confidence": 0.95,
                "match": true,
                "person_id": "person_001",
                "similarity": 0.87,
                "face_id": "uuid"
            }
        ],
        "processing_time": 0.123
    }
    ```
    """
    await websocket.accept()
    print(f"WebSocket connected for app_id: {app_id}")
    
    try:
        while True:
            # Try to receive binary data first
            try:
                # Check message type
                message = await websocket.receive()
                
                if "bytes" in message:
                    # Binary mode (optimized)
                    image_data = message["bytes"]
                    current_threshold = threshold  # Use query param
                elif "text" in message:
                    # JSON mode (fallback for compatibility)
                    data = json.loads(message["text"])
                    image_base64 = data.get("image")
                    current_threshold = data.get("threshold", threshold)
                    
                    if not image_base64:
                        await websocket.send_json({
                            "error": "No image provided",
                            "face_count": 0,
                            "faces": []
                        })
                        continue
                    
                    image_data = base64.b64decode(image_base64)
                else:
                    await websocket.send_json({
                        "error": "Invalid message format",
                        "face_count": 0,
                        "faces": []
                    })
                    continue
                    
                # Open image from binary data
                image = Image.open(BytesIO(image_data))
                
                # Convert to numpy array
                img_array = np.array(image)
                
                # Detect faces
                import time
                start_time = time.time()
                
                detected_faces = face_engine.detect_faces(
                    img_array,
                    min_confidence=0.5
                )
                
                # Search for matches in database
                db = SessionLocal()
                try:
                    response_faces = []
                    
                    for face in detected_faces:
                        face_data = {
                            "bbox": face["bbox"].tolist() if isinstance(face["bbox"], np.ndarray) else face["bbox"],
                            "confidence": float(face["confidence"]),
                            "match": False
                        }
                        
                        # Search in database
                        if "embedding" in face:
                            search_results = face_engine.search_in_database(
                                db=db,
                                app_id=app_id,
                                feature_vector=face["embedding"],
                                top_k=1,
                                threshold=current_threshold
                            )
                            
                            if search_results:
                                best_match = search_results[0]
                                face_data.update({
                                    "match": True,
                                    "person_id": best_match["person_id"],
                                    "similarity": float(best_match["similarity"]),
                                    "face_id": str(best_match["face_id"])
                                })
                        
                        response_faces.append(face_data)
                    
                    processing_time = time.time() - start_time
                    
                    # Send response
                    await websocket.send_json({
                        "face_count": len(detected_faces),
                        "faces": response_faces,
                        "processing_time": round(processing_time, 3)
                    })
                    
                finally:
                    db.close()
                    
            except Exception as e:
                await websocket.send_json({
                    "error": f"Processing error: {str(e)}",
                    "face_count": 0,
                    "faces": []
                })
                
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for app_id: {app_id}")
    except Exception as e:
        print(f"WebSocket error for app_id {app_id}: {e}")
        try:
            await websocket.close()
        except:
            pass
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.send_json({
                "error": f"Connection error: {str(e)}",
                "face_count": 0,
                "faces": []
            })
        except:
            pass
