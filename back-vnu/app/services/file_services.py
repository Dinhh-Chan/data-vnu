from fastapi import HTTPException, status
from minio import Minio 
from fastapi.responses import StreamingResponse
from minio import S3Error
import os 
import uuid
import io 

class fileServices(object):
    @staticmethod 
    async def upload_file_to_minio(file, custom_filename, description, file_type, minio_client):
        bucket_name = os.getenv('MINIO_BUCKET', 'mybucket')

        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)

        file_extension = file.filename.split(".")[-1]
        filename_final = custom_filename if custom_filename else str(uuid.uuid4())
        filename_final = f"{filename_final}.{file_extension}"

        try: 
            file_data = await file.read()
            file_like_object = io.BytesIO(file_data)

            minio_client.put_object(
                bucket_name=bucket_name,
                object_name=filename_final,
                data=file_like_object, 
                length=len(file_data),
                content_type=file.content_type,
                metadata={
                    "file_type": file_type or "undefined",
                    "description": description or "none"
                }
            )

            file_url = f"http://{os.getenv('MINIO_ENDPOINT')}/{bucket_name}/{filename_final}"

            return {
                "filename": filename_final,
                "url": file_url,
                "description": description or "none",
                "file_type": file_type or "undefined"
            }

        except S3Error as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error uploading file: {e}",
            )
    @staticmethod
    async def download_file( file_name, minio_client ):
        bucket_name = os.getenv('MINIO_BUCKET', 'mybucket')
        try:
            minio_client.stat_object(bucket_name, file_name)
            file_data = minio_client.get_object(bucket_name, file_name)
            response = StreamingResponse(
                file_data.stream(32 * 1024),
                media_type='application/octet-stream'
            )
            response.headers["Content-Disposition"] = f"attachment; filename={file_name}"

            return response

        except S3Error as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File not found: {e}",
    )
    @staticmethod
    async def get_all_files(minio_client):
        bucket_name = os.getenv('MINIO_BUCKET', 'mybucket')
        try :
            if not minio_client.bucket_exists(bucket_name):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Bucket not found"
                )
            objects = minio_client.list_objects(bucket_name)
            files = []
            for obj in objects:
                files.append({
                    "file_name": obj.object_name,
                    "size": obj.size,
                    "last_modified": obj.last_modified,
                    "url": f"http://{os.getenv('MINIO_ENDPOINT')}/{bucket_name}/{obj.object_name}"
                })
            return files
        except S3Error as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving files: {e}",
            )