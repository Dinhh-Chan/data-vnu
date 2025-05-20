from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_connections import DBConnection
from fastapi import HTTPException, status
from app.dto.db_connection import DBConnectionCreate, DBConnectionUpdate
from app.models.db_connections import DBConnection
from sqlalchemy.orm import Session 
class DBConfigService:
    @staticmethod 
    async def get_acttive_db_connections(db: AsyncSession):
        try:
            stmt = select(DBConnection).where(DBConnection.is_active == True)
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving active database connections: {str(e)}",
            )

    @staticmethod
    async def get_all_db_connections(db: AsyncSession):
        try:
            stmt = select(DBConnection)
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving all database connections: {str(e)}",
            )
    @staticmethod
    async def create_db_connection(db: Session, db_connection_data: DBConnectionCreate):
        try:
            db_connection = DBConnection(**db_connection_data.dict())
            db.add(db_connection)
            await db.commit()
            await db.refresh(db_connection)
            return db_connection
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating database connection: {str(e)}",
            )
    @staticmethod
    async def update_db_connection(
        db: AsyncSession, connection_id: int, update_data: DBConnectionUpdate
    ):
        try:
            db_obj = await db.get(DBConnection, connection_id)
            if not db_obj:
                raise HTTPException(status_code=404, detail="Connection not found")

            for field, value in update_data.dict(exclude_unset=True).items():
                setattr(db_obj, field, value)

            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error updating database connection: {str(e)}"
            )