from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Depends
from minio import Minio
from minio.error import S3Error
from app.services.minio_services import minioClass
from app.services.file_services import fileServices
from app.dto.files import FileCreate, FileSchema
from app.services.db_file_service import DBFileService
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
import os 
import uuid

router = APIRouter()

@router.post(
    "/upload",
    response_model=FileSchema,
    status_code=201,
    summary="Upload file to MinIO and save metadata to DB"
)
async def upload_and_save(
    file: UploadFile = File(...),
    custom_name: str = Form(None),
    description: str = Form(None),
    minio_client: Minio = Depends(minioClass.get_minio_client),
    db: AsyncSession = Depends(get_db)
):
    # 1. Upload lên MinIO, MinioService sẽ tự lấy extension
    info = await fileServices.upload_to_minio(
        file=file,
        custom_filename=custom_name,
        description=description,
        minio_client=minio_client
    )

    # 2. Chuẩn bị schema và lưu vào DB
    file_create = FileCreate(
        file_name=info["file_name"],
        file_type=info["file_type"],
        file_size=info["file_size"],
        description=info["description"],
        url=info["url"]
    )
    saved = await DBFileService.create(db, file_create)
    return saved

@router.get(
    "/files",
    response_model=list[FileSchema],
    summary="List all uploaded files"
)
async def list_files(db: AsyncSession = Depends(get_db)):
    return await DBFileService.list_all(db)
@router.post(
    "/download",
    summary="Download a file from MinIO",
)
async def download_file(
    file_name: str = Form(...),
    minio_client: Minio = Depends(minioClass.get_minio_client)
):
    try:
        return await fileServices.download_file(file_name, minio_client)
    except HTTPException as e:
        raise e
    except S3Error as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File not found: {e}"
        )