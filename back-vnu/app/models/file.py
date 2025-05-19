from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from app.db.base_class import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=False)
    description = Column(Text)
    url = Column(String(255), nullable=False)
