from minio import Minio
from minio.error import S3Error
import os 
import uuid

class minioClass(object):
    @staticmethod
    def get_minio_client():
        return Minio(
            endpoint=os.getenv("MINIO_ENDPOINT"),
            access_key=os.getenv("MINIO_ACCESS_KEY"),
            secret_key=os.getenv("MINIO_SECRET_KEY"),
            secure= False
        )