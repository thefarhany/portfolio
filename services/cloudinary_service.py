import cloudinary
import cloudinary.uploader
from fastapi import HTTPException, UploadFile


def upload_image(file: UploadFile):
    try:
        result = cloudinary.uploader.upload(
            file.file, 
            folder="portfolio" 
        )
        return result.get("secure_url")
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Gagal nge-upload gambar ke Cloudinary bro: {str(e)}"
        )