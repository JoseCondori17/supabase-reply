from fastapi import APIRouter, Depends

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

@router.get("/", status_code=200)
async def get_all_tables():
    pass

@router.get("/{table_id}", status_code=200)
async def get_table_by_id(table_id: str):
    pass

@router.put("/{table_id}", status_code=200)
async def replace_table(table_id: str):
    pass

@router.patch("/{table_id}", status_code=200)
async def update_table_partially(table_id: str):
    pass

@router.delete("/{table_id}", status_code=204)
async def delete_table(table_id: str):
    pass