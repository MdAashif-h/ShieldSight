from fastapi import APIRouter, UploadFile, File, HTTPException, Request
import os
import uuid
import httpx
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
        
        # Upload to ImgBB
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.imgbb.com/1/upload",
                data={
                    "key": IMGBB_API_KEY,
                    "name": f"avatar_{uuid.uuid4().hex[:8]}"
                },
                files={"image": (file.filename, content, file.content_type)}
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "url": data["data"]["url"],
                    "filename": data["data"]["image"]["filename"],
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                raise HTTPException(status_code=500, detail="Failed to upload image to host")
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")
