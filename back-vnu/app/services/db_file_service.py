# app/services/db_file_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.file import File
from app.dto.files import FileCreate

class DBFileService:
    @staticmethod
    async def create(db: AsyncSession, file_data: FileCreate):
        new = File(**file_data.dict())
        db.add(new)
        await db.commit()
        await db.refresh(new)
        return new

    @staticmethod
    async def list_all(db: AsyncSession):
        result = await db.execute(select(File))
        return result.scalars().all()
