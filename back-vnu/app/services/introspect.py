from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
from pymongo import MongoClient
from fastapi import HTTPException
from app.models.db_connections import DBConnection


class DBIntrospectionService:

    @staticmethod
    def build_connection_uri(db: DBConnection) -> str:
        if db.db_type == "postgresql":
            return f"postgresql+psycopg2://{db.username}:{db.password}@{db.host}:{db.port}/{db.database_name}"
        elif db.db_type == "mysql":
            return f"mysql+pymysql://{db.username}:{db.password}@{db.host}:{db.port}/{db.database_name}"
        elif db.db_type == "sqlserver":
            return (
                f"mssql+pyodbc://{db.username}:{db.password}@{db.host},{db.port}/"
                f"{db.database_name}?driver=ODBC+Driver+17+for+SQL+Server"
            )
        elif db.db_type == "mongodb":
            return f"mongodb://{db.username}:{db.password}@{db.host}:{db.port}/{db.database_name}"
        else:
            raise ValueError(f"Unsupported database type: {db.db_type}")

    @staticmethod
    def introspect_sql_db(uri: str):
        try:
            engine = create_engine(uri)
            inspector = inspect(engine)

            result = []
            for table_name in inspector.get_table_names():
                columns = inspector.get_columns(table_name)
                column_info = [
                    {
                        "name": col["name"],
                        "type": str(col["type"]),
                        "nullable": col.get("nullable"),
                        "default": col.get("default")
                    }
                    for col in columns
                ]
                result.append({
                    "table_name": table_name,
                    "columns": column_info
                })

            return result
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"SQL introspection failed: {str(e)}")

    @staticmethod
    def introspect_mongodb(uri: str, database_name: str):
        try:
            client = MongoClient(uri)
            db = client[database_name]

            result = []
            for collection_name in db.list_collection_names():
                sample = db[collection_name].find_one()
                fields = [{"name": k, "type": type(v).__name__} for k, v in sample.items()] if sample else []
                result.append({
                    "collection_name": collection_name,
                    "fields": fields
                })

            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"MongoDB introspection failed: {str(e)}")

    @staticmethod
    def introspect_database(db_connection: DBConnection):
        uri = DBIntrospectionService.build_connection_uri(db_connection)

        if db_connection.db_type in {"postgresql", "mysql", "sqlserver"}:
            return {
                "type": db_connection.db_type,
                "structures": DBIntrospectionService.introspect_sql_db(uri)
            }
        elif db_connection.db_type == "mongodb":
            return {
                "type": db_connection.db_type,
                "structures": DBIntrospectionService.introspect_mongodb(uri, db_connection.database_name)
            }
        else:
            raise HTTPException(status_code=400, detail="Unsupported database type")
