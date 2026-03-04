from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid
from datetime import datetime

router = APIRouter(prefix="/user", tags=["User"])

UPLOAD_DIR = "uploads/avatars"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-avatar")
async def upload_avatar(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Save file
    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save image: {str(e)}")
    
    # Return the URL (assuming backend runs on port 8000)
    # In production, this should use the actual domain
    avatar_url = f"http://localhost:8000/uploads/avatars/{filename}"
    
    return {
        "url": avatar_url,
        "filename": filename,
        "timestamp": datetime.utcnow().isoformat()
    }
