from fastapi import APIRouter, Depends, HTTPException, status
from app.services.db_config_service import DBConfigService
from app.db.session import get_db
from app.models.db_connections import DBConnection
from app.dto.db_connection import DBConnectionSchema ,DBConnectionCreate, DBConnectionUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.introspect import DBIntrospectionService
from sqlalchemy.orm import Session 
router = APIRouter()

@router.get("/active", response_model=list[DBConnectionSchema])
async def get_active_db_connections(
    db: Session = Depends(get_db),
):
    """
    Lấy danh sách các kết nối cơ sở dữ liệu đang hoạt động.
    """
    try:
        db_connections =await DBConfigService.get_acttive_db_connections(db)
        return db_connections
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving active database connections: {str(e)}",
        )
@router.get("/", response_model=list[DBConnectionSchema])
async def get_all_db_connections(
    db: Session = Depends(get_db),
):
    """
    Lấy danh sách tất cả các kết nối cơ sở dữ liệu.
    """
    try:
        db_connections = await DBConfigService.get_all_db_connections(db)
        return db_connections
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving all database connections: {str(e)}",
        )
@router.post("/", response_model=DBConnectionSchema, status_code=201)
async def create_db_connection(
    db_connection_data: DBConnectionCreate,
    db: Session = Depends(get_db),
):
    return await DBConfigService.create_db_connection(db, db_connection_data)
@router.get("/introspect/{connection_id}")
async def introspect_database(connection_id: int, db: AsyncSession = Depends(get_db)):
    db_connection = await db.get(DBConnection, connection_id)
    if not db_connection:
        raise HTTPException(status_code=404, detail="Database connection not found")

    return DBIntrospectionService.introspect_database(db_connection)
@router.put("/{connection_id}", response_model=DBConnectionSchema)
async def update_db_connection(
    connection_id: int,
    update_data: DBConnectionUpdate,
    db: Session = Depends(get_db),
):
    return await DBConfigService.update_db_connection(db, connection_id, update_data)