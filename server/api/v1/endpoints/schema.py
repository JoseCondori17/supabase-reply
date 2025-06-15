from fastapi import APIRouter, HTTPException
from server.api.v1.dependencies import SchemaServiceDep

router = APIRouter()

"""
HTTP    ROUTE       DESCRIPTION         CODE
POST    /           Create sc           201
GET     /           Get all sc          200
GET     /{id}       Get sc by id        200
PUT     /{id}       Replace all data    200
PATH    /{id}       Partial update      200
DELETE  /{id}       Delete sc           204
"""

@router.post("/", status_code=201)
async def create_schema():
    pass

@router.get("/{database_name}", status_code=200)
async def get_all_schemas(sch_service: SchemaServiceDep, database_name: str):
    try:
        schemas = sch_service.get_schemas_json(database_name)
        return {
            "success": True,
            "data": schemas
        }
    except Exception as e:
        error_msg = f"Error obtaining schemas: {str(e)}"
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": error_msg
            }
        )

@router.get("/{database_name}/{schema_name}", status_code=200)
async def get_schema_by_name(sch_service: SchemaServiceDep, database_name: str, schema_name: str):
    try:
        schema = sch_service.get_schema_json(database_name, schema_name)
        return {
            "success": True,
            "data": schema
        }
    except Exception as e:
        error_msg = f"Error obtaining schema: {str(e)}"
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": error_msg
            }
        )

@router.put("/{schema_name}", status_code=200)
async def replace_schema(sch_service: SchemaServiceDep, schema_name: str):
    pass

@router.patch("/{schema_name}", status_code=200)
async def update_schema_partially(sch_service: SchemaServiceDep, schema_name: str):
    pass

@router.delete("/{schema_name}", status_code=204)
async def delete_schema(sch_service: SchemaServiceDep, schema_name: str):
    pass