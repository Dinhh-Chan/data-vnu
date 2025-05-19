# app/schemas/file.py
from pydantic import BaseModel
from typing import Optional

class FileCreate(BaseModel):
    file_name: str
    file_type: str
    file_size: int
    description: Optional[str]
    url: str

class FileSchema(FileCreate):
    id: int

    class Config:
        from_attributes = True  # tương đương orm_mode=True trong Pydantic v1
