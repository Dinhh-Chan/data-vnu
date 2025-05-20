from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, JSON
from app.db.base_class import Base
from datetime import datetime
class ExternalAPIEndpoint(Base):
    __tablename__ = "external_api_endpoints"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)
    base_url = Column(String(255), nullable=False)
    swagger_url = Column(String(255), nullable=False)
    default_headers = Column(Text) 
    is_active = Column(Boolean, default=True)
    path = Column(String(255), nullable=False)   
    method = Column(String(10), nullable=False)     
    summary = Column(String(255))
    description = Column(Text)
    parameters = Column(JSON)
    request_body = Column(JSON)
    responses = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
