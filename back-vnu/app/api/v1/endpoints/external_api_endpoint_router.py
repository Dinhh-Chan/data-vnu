from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dto.external_api_endpoint import ExternalAPIEndpointCreate, ExternalAPIEndpointUpdate, ExternalAPIEndpointSchema
from app.services.external_api_endpoint_service import ExternalAPIEndpointService
from app.models.external_api_endpoints import ExternalAPIEndpoint
import httpx
import json

router = APIRouter(prefix="/external-endpoints", tags=["External API Endpoints"])

@router.post("/", response_model=ExternalAPIEndpointSchema)
async def create_endpoint(data: ExternalAPIEndpointCreate, db: AsyncSession = Depends(get_db)):
    return await ExternalAPIEndpointService.create(db, data)

@router.put("/{endpoint_id}", response_model=ExternalAPIEndpointSchema)
async def update_endpoint(endpoint_id: int, data: ExternalAPIEndpointUpdate, db: AsyncSession = Depends(get_db)):
    return await ExternalAPIEndpointService.update(db, endpoint_id, data)

@router.delete("/{endpoint_id}")
async def delete_endpoint(endpoint_id: int, db: AsyncSession = Depends(get_db)):
    return await ExternalAPIEndpointService.delete(db, endpoint_id)

@router.get("/", response_model=list[ExternalAPIEndpointSchema])
async def get_all_endpoints(db: AsyncSession = Depends(get_db)):
    return await ExternalAPIEndpointService.get_all(db)

@router.get("/{endpoint_id}", response_model=ExternalAPIEndpointSchema)
async def get_endpoint(endpoint_id: int, db: AsyncSession = Depends(get_db)):
    return await ExternalAPIEndpointService.get_by_id(db, endpoint_id)

@router.api_route("/proxy/{endpoint_id}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_endpoint(endpoint_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    endpoint = await db.get(ExternalAPIEndpoint, endpoint_id)
    if not endpoint or not endpoint.is_active:
        raise HTTPException(status_code=404, detail="Endpoint not found")

    url = f"{endpoint.base_url.rstrip('/')}/{endpoint.path.lstrip('/')}"
    method = endpoint.method.upper()

    try:
        body = await request.json() if method in ("POST", "PUT", "PATCH") else None
        query = dict(request.query_params)

        # Chỉ giữ lại headers an toàn
        incoming_headers: Headers = request.headers
        headers = {
            "User-Agent": incoming_headers.get("user-agent", "fastapi-proxy"),
            "Accept": "application/json",
        }

        # Thêm headers mặc định từ DB nếu có
        if endpoint.default_headers:
            import json
            headers.update(json.loads(endpoint.default_headers))

        async with httpx.AsyncClient() as client:
            resp = await client.request(
                method=method,
                url=url,
                headers=headers,
                params=query,
                json=body
            )

        return {
            "status_code": resp.status_code,
            "body": resp.json() if "application/json" in resp.headers.get("content-type", "") else resp.text,
            "headers": dict(resp.headers),
        }

    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Proxy error: {str(e)}")