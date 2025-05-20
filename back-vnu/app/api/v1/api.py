from fastapi import APIRouter

from app.api.v1.endpoints import users, auth, file, db_connection, external_api_endpoint_router

api_router = APIRouter()

# Include all API endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(file.router, prefix="/file", tags=["upload"])
api_router.include_router(db_connection.router, prefix="/db", tags=["db_connection"])
api_router.include_router(external_api_endpoint_router.router, prefix="/swagger-api", tags=["db_connection"])
