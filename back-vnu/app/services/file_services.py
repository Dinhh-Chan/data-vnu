from fastapi import HTTPException, status
from minio import Minio 
from fastapi.responses import StreamingResponse
from minio import S3Error
import os 
import uuid
import io 

class fileServices(object):
    @staticmethod 
    async def upload_to_minio(file, custom_filename, description, minio_client):
        bucket = os.getenv('MINIO_BUCKET', 'mybucket')
        if not minio_client.bucket_exists(bucket):
            minio_client.make_bucket(bucket)

        # Lấy extension tự động
        original = file.filename
        ext = original.rsplit(".", 1)[-1].lower()

        name = custom_filename or str(uuid.uuid4())
        final_name = f"{name}.{ext}"

        data = await file.read()
        bio = io.BytesIO(data)
        try:
            minio_client.put_object(
                bucket,
                final_name,
                data=bio,
                length=len(data),
                content_type=file.content_type
            )
        except S3Error as e:
            raise HTTPException(status_code=500, detail=str(e))

        return {
            "file_name": final_name,
            "file_type": ext,               # <-- extension ở đây
            "description": description,
            "file_size": len(data),
            "url": f"http://{os.getenv('MINIO_ENDPOINT')}/{bucket}/{final_name}"
        }
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