from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from typing import List
from services import cloudinary_service
from core.security import verify_token

router = APIRouter(
    prefix="/api/upload",
    tags=["Uploads"]
)

@router.post("/image")
def upload_single_image(
    file: UploadFile = File(...),
    user_data: dict = Depends(verify_token) 
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Wah, yang lu upload bukan gambar bro!")
        
    image_url = cloudinary_service.upload_image(file)
    
    return {
        "message": "Upload sukses bro!",
        "image_url": image_url
    }
    
@router.post("/images")
def upload_multiple_images(
    files: List[UploadFile] = File(...),
    user_data: dict = Depends(verify_token)
):
    uploaded_urls = []
    
    for file in files:
        if file.content_type.startswith("image/"):
            url = cloudinary_service.upload_image(file)
            uploaded_urls.append(url)
            
    if not uploaded_urls:
        raise HTTPException(status_code=400, detail="Wah, gak ada satupun file gambar yang valid bro!")
        
    return {
        "message": f"Mantap, {len(uploaded_urls)} gambar berhasil diupload!",
        "image_urls": uploaded_urls
    }