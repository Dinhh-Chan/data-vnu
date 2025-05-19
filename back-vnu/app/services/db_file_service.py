# app/services/db_file_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.file import File
from app.dto.files import FileCreate

class DBFileService:
    @staticmethod
    async def create(db: AsyncSession, file_data: FileCreate):
        stmt = select(File).where(File.file_name == file_data.file_name)
        result = await db.execute(stmt)
        exists = result.scalars().first()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File already exists"
            )
        new = File(**file_data.dict())
        db.add(new)
        await db.commit()
        await db.refresh(new)
        return new
    @staticmethod
    async def list_all(db: AsyncSession):
        result = await db.execute(select(File))
        return result.scalars().all()
    
