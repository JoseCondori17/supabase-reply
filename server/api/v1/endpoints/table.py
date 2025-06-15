from fastapi import APIRouter, HTTPException
from server.api.v1.dependencies import TableServiceDep

router = APIRouter()

"""
HTTP    ROUTE       DESCRIPTION         CODE
POST    /           Create tab          201
GET     /           Get all tab         200
GET     /{id}       Get tab by id       200
PUT     /{id}       Replace all data    200
PATH    /{id}       Partial update      200
DELETE  /{id}       Delete tab          204
"""

@router.post("/", status_code=201)
async def create_table():
    pass

@router.get("/{database_name}/{schema_name}", status_code=200)
async def get_all_tables(tab_service: TableServiceDep, database_name: str, schema_name: str):
    try:
        tables = tab_service.get_tables_json(database_name, schema_name)
        return {
            "success": True,
            "data": tables
        }
    except Exception as e:
        error_msg = f"Error obtaining tables: {str(e)}"
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": error_msg
            }
        )

@router.get("/{table_name}", status_code=200)
async def get_table_by_name(tab_service: TableServiceDep, database_name: str, schema_name: str, table_name: str):
    try:
        table = tab_service.get_table_json(database_name, schema_name, table_name)
        return {
            "success": True,
            "data": table
        }
    except Exception as e:
        error_msg = f"Error obtaining table: {str(e)}"
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": error_msg
            }
        )

@router.put("/{table_name}", status_code=200)
async def replace_table(tab_service: TableServiceDep, table_name: str):
    pass

@router.patch("/{table_name}", status_code=200)
async def update_table_partially(tab_service: TableServiceDep, table_name: str):
    pass

@router.delete("/{table_name}", status_code=204)
async def delete_table(tab_service: TableServiceDep, table_name: str):
    pass