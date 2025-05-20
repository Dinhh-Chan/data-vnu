from pydantic import BaseModel
from typing import Optional, List, Dict

class ExternalAPIEndpointCreate(BaseModel):
    name: str
    base_url: str
    swagger_url: str
    default_headers: Optional[str] = "{}"
    is_active: Optional[bool] = True
    path: str
    method: str
    summary: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[List[Dict]] = []
    request_body: Optional[Dict] = {}
    responses: Optional[Dict] = {}

class ExternalAPIEndpointUpdate(BaseModel):
    name: Optional[str]
    base_url: Optional[str]
    swagger_url: Optional[str]
    default_headers: Optional[str]
    is_active: Optional[bool]
    path: Optional[str]
    method: Optional[str]
    summary: Optional[str]
    description: Optional[str]
    parameters: Optional[List[Dict]]
    request_body: Optional[Dict]
    responses: Optional[Dict]

class ExternalAPIEndpointSchema(ExternalAPIEndpointCreate):
    id: int

    class Config:
        orm_mode = True