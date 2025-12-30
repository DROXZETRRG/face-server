#!/usr/bin/env python3
"""
Example script demonstrating Face Server API usage.

This script shows how to:
1. Create an application
2. Register a face
3. Search for similar faces
4. List and manage faces
"""
import requests
import json
from pathlib import Path


# API Base URL
BASE_URL = "http://localhost:8000/api/v1"


def create_application(app_code: str, app_name: str):
    """Create a new application."""
    print(f"\n📝 Creating application: {app_code}")
    
    response = requests.post(
        f"{BASE_URL}/applications",
        json={
            "app_code": app_code,
            "app_name": app_name
        }
    )
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ Application created successfully!")
        print(f"   ID: {data['id']}")
        print(f"   Code: {data['app_code']}")
        print(f"   Name: {data['app_name']}")
        return data
    else:
        print(f"❌ Failed to create application: {response.text}")
        return None


def list_applications():
    """List all applications."""
    print("\n📋 Listing applications...")
    
    response = requests.get(f"{BASE_URL}/applications")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['total']} application(s)")
        for app in data['items']:
            print(f"   - {app['app_code']}: {app['app_name']} (ID: {app['id']})")
        return data['items']
    else:
        print(f"❌ Failed to list applications: {response.text}")
        return []


def register_face(app_id: str, person_id: str, image_path: str, metadata: dict = None):
    """Register a face."""
    print(f"\n👤 Registering face for person: {person_id}")
    
    # Check if image file exists
    if not Path(image_path).exists():
        print(f"❌ Image file not found: {image_path}")
        print("   Please provide a valid image path or create a dummy image")
        return None
    
    # Prepare form data
    files = {
        'image': open(image_path, 'rb')
    }
    data = {
        'app_id': app_id,
        'person_id': person_id,
    }
    
    if metadata:
        data['metadata'] = json.dumps(metadata)
    
    response = requests.post(
        f"{BASE_URL}/faces",
        files=files,
        data=data
    )
    
    if response.status_code == 201:
        face_data = response.json()
        print(f"✅ Face registered successfully!")
        print(f"   Face ID: {face_data['id']}")
        print(f"   Person ID: {face_data['person_id']}")
        print(f"   Image URL: {face_data['image_url']}")
        return face_data
    else:
        print(f"❌ Failed to register face: {response.text}")
        return None


def list_faces(app_id: str, person_id: str = None):
    """List faces."""
    print(f"\n📋 Listing faces for application...")
    
    params = {'app_id': app_id}
    if person_id:
        params['person_id'] = person_id
    
    response = requests.get(f"{BASE_URL}/faces", params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['total']} face(s)")
        for face in data['items']:
            print(f"   - Person: {face['person_id']}, Face ID: {face['id']}")
        return data['items']
    else:
        print(f"❌ Failed to list faces: {response.text}")
        return []


def search_faces(app_id: str, image_path: str, top_k: int = 10, threshold: float = 0.6):
    """Search for similar faces."""
    print(f"\n🔍 Searching for similar faces...")
    
    # Check if image file exists
    if not Path(image_path).exists():
        print(f"❌ Image file not found: {image_path}")
        print("   Please provide a valid image path")
        return None
    
    files = {
        'image': open(image_path, 'rb')
    }
    data = {
        'app_id': app_id,
        'top_k': top_k,
        'threshold': threshold
    }
    
    response = requests.post(
        f"{BASE_URL}/faces/search",
        files=files,
        data=data
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Search completed in {result['query_time_ms']:.2f}ms")
        print(f"   Found {len(result['results'])} match(es)")
        for i, match in enumerate(result['results'], 1):
            print(f"   {i}. Person: {match['person_id']}, Similarity: {match['similarity']:.3f}")
        return result
    else:
        print(f"❌ Failed to search faces: {response.text}")
        return None


def main():
    """Main demonstration function."""
    print("="*60)
    print("Face Server API Usage Example")
    print("="*60)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code != 200:
            print("❌ Server is not responding correctly")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please ensure it's running:")
        print("   uvicorn app.main:app --reload")
        return
    
    print("✅ Server is running")
    
    # 1. Create an application
    app = create_application("demo_app", "Demo Application")
    if not app:
        return
    
    app_id = app['id']
    
    # 2. List applications
    list_applications()
    
    # 3. Register faces (requires actual image files)
    print("\n" + "="*60)
    print("📸 Face Registration")
    print("="*60)
    print("To register faces, you need to provide image files.")
    print("Example:")
    print("  register_face(app_id, 'person_001', 'path/to/image.jpg', {'name': 'John Doe'})")
    
    # If you have test images, uncomment and modify:
    # register_face(app_id, "person_001", "test_images/person1.jpg", {"name": "John Doe"})
    # register_face(app_id, "person_002", "test_images/person2.jpg", {"name": "Jane Smith"})
    
    # 4. List faces
    list_faces(app_id)
    
    # 5. Search faces (requires actual image file)
    print("\n" + "="*60)
    print("🔍 Face Search")
    print("="*60)
    print("To search for faces, you need to provide a query image.")
    print("Example:")
    print("  search_faces(app_id, 'path/to/query.jpg', top_k=5, threshold=0.7)")
    
    # If you have test images, uncomment and modify:
    # search_faces(app_id, "test_images/query.jpg", top_k=5, threshold=0.7)
    
    print("\n" + "="*60)
    print("✅ Demo Complete!")
    print("="*60)
    print("\n📚 API Documentation: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
