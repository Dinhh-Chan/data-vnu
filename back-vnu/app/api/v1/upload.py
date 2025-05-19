from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from minio import Minio
from minio.error import S3Error
from app.services.minio_services import minioClass
from app.services.file_services import fileServices
import os 
import uuid

router = APIRouter()

@router.post("/upload")
def upload_file_minio(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    minio_client: Minio = minioClass.get_minio_client(),
):
    response = fileServices.upload_file_to_minio(
        file=file,
        custom_filename=name,   
        description=description,
        file_type=category,
        minio_client=minio_client
    )
    if not response:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="File upload failed",
        )
    return {
        "filename": response["filename"],
        "url": response["url"],
        "description": response["description"],
        "file_type": response["file_type"]
    }
    