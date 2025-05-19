from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Depends
from minio import Minio
from app.services.minio_services import minioClass
from app.services.file_services import fileServices

router = APIRouter()

@router.post("/upload")
async def upload_file_minio(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    minio_client: Minio = Depends(minioClass.get_minio_client), 
):
    response = await fileServices.upload_file_to_minio(
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
@router.get("/download/{file_name}")
async def download_file(file_name: str, minio_client: Minio = Depends(minioClass.get_minio_client)):
    try:
        response = await fileServices.download_file(file_name, minio_client)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error downloading file: {str(e)}",
        )
@router.get("/list")
async def list_files(minio_client: Minio = Depends(minioClass.get_minio_client)):
    try:
        files = await fileServices.get_all_files(minio_client)
        return files
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing files: {str(e)}",
        )
