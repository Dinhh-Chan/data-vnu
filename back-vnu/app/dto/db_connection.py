from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DBConnectionSchema(BaseModel):
    id: int
    db_type: str
    host: str
    port: int
    database_name: str
    username: Optional[str]
    password: Optional[str]
    extra_uri: Optional[str]
    is_active: bool
    created_at: Optional[datetime]

    class Config:
        from_attributes = True  # Pydantic v2 (tên mới của orm_mode)
class DBConnectionCreate(BaseModel):
    db_type: str
    host: str
    port: int
    database_name: str
    username: Optional[str] = None
    password: Optional[str] = None
    extra_uri: Optional[str] = None
    is_active: Optional[bool] = True