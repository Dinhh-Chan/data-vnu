from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from app.db.base_class import Base
from datetime import datetime

class ExternalAPI(Base):
    __tablename__ = "external_apis"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    base_url = Column(String(255), nullable=False)
    swagger_url = Column(String(255), nullable=False)
    default_headers = Column(Text)
    is_active = Column(Boolean, default=True)