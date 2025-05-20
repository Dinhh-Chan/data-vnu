from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.external_api_endpoints import ExternalAPIEndpoint
from app.dto.external_api_endpoint import ExternalAPIEndpointCreate, ExternalAPIEndpointUpdate

class ExternalAPIEndpointService:
    @staticmethod
    async def create(db: AsyncSession, data: ExternalAPIEndpointCreate):
        endpoint = ExternalAPIEndpoint(**data.dict())
        db.add(endpoint)
        await db.commit()
        await db.refresh(endpoint)
        return endpoint

    @staticmethod
    async def update(db: AsyncSession, endpoint_id: int, data: ExternalAPIEndpointUpdate):
        endpoint = await db.get(ExternalAPIEndpoint, endpoint_id)
        if not endpoint:
            raise HTTPException(status_code=404, detail="Endpoint not found")

        for field, value in data.dict(exclude_unset=True).items():
            setattr(endpoint, field, value)

        await db.commit()
        await db.refresh(endpoint)
        return endpoint

    @staticmethod
    async def delete(db: AsyncSession, endpoint_id: int):
        endpoint = await db.get(ExternalAPIEndpoint, endpoint_id)
        if not endpoint:
            raise HTTPException(status_code=404, detail="Endpoint not found")
        await db.delete(endpoint)
        await db.commit()
        return {"detail": "Deleted successfully"}

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(ExternalAPIEndpoint))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, endpoint_id: int):
        endpoint = await db.get(ExternalAPIEndpoint, endpoint_id)
        if not endpoint:
            raise HTTPException(status_code=404, detail="Endpoint not found")
        return endpoint
