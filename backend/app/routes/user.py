from fastapi import APIRouter, UploadFile, File, HTTPException, Request
import os
import uuid
import base64
import requests # Using requests instead of httpx for simpler multipart
from datetime import datetime

router = APIRouter(prefix="/user", tags=["User"])

# Using ImgBB for free, ephemeral-safe image hosting
IMGBB_API_KEY = "6bedf6bf3edba6ddefdb5ad9f018e6c7" # Free tier key

@router.post("/upload-avatar")
async def upload_avatar(request: Request, file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        content = await file.read()
        
        # Upload to ImgBB via base64 encoding (most reliable for their API)
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": IMGBB_API_KEY,
            "image": base64.b64encode(content).decode('utf-8'),
            "name": f"avatar_{uuid.uuid4().hex[:8]}"
        }
        
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "url": data["data"]["url"],
                "filename": data["data"]["image"]["filename"],
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail=f"Failed to upload image to host: {response.text}")
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")
