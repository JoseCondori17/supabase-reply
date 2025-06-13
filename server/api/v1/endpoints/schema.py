from fastapi import APIRouter, Depends

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

@router.get("/", status_code=200)
async def get_all_schemas():
    pass

@router.get("/{schema_id}", status_code=200)
async def get_schema_by_id(schema_id: str):
    pass

@router.put("/{schema_id}", status_code=200)
async def replace_schema(schema_id: str):
    pass

@router.patch("/{schema_id}", status_code=200)
async def update_schema_partially(schema_id: str):
    pass

@router.delete("/{schema_id}", status_code=204)
async def delete_schema(schema_id: str):
    pass