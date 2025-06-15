from fastapi import APIRouter, HTTPException
from server.api.v1.dependencies import DatabaseServiceDep

router = APIRouter()

"""
HTTP    ROUTE       DESCRIPTION         CODE
POST    /           Create db           201
GET     /           Get all db          200
GET     /{id}       Get db by id        200
PUT     /{id}       Replace all data    200
PATH    /{id}       Partial update      200
DELETE  /{id}       Delete db           204
"""

@router.post("/", status_code=201)
async def create_database():
    pass

@router.get("/", status_code=200)
async def get_all_databases(db_service: DatabaseServiceDep):
    try:
        databases = db_service.get_databases_json()
        return {
            "success": True,
            "data": databases
        }
    except Exception as e:
        error_msg = f"Error obtaining databases: {str(e)}"
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": error_msg
            }
        )

@router.get("/{database_name}", status_code=200)
async def get_database_by_name(db_service: DatabaseServiceDep, database_name: str):
    try:
        databases = db_service.get_database_json(database_name)
        return {
            "success": True,
            "data": databases
        }
    except Exception as e:
        error_msg = f"Error obtaining database {database_name}: {str(e)}"
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": error_msg
            }
        )

@router.put("/{database_name}", status_code=200)
async def replace_database(db_service: DatabaseServiceDep, database_name: str):
    pass

@router.patch("/{database_name}", status_code=200)
async def update_database_partially(db_service: DatabaseServiceDep, database_name: str):
    pass

@router.delete("/{database_name}", status_code=204)
async def delete_database(db_service: DatabaseServiceDep, database_name: str):
    pass

