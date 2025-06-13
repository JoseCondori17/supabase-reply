from fastapi import APIRouter, Depends

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
async def get_all_databases():
    pass

@router.get("/{database_id}", status_code=200)
async def get_database_by_id(database_id: str):
    pass

@router.put("/{database_id}", status_code=200)
async def replace_database(database_id: str):
    pass

@router.patch("/{database_id}", status_code=200)
async def update_database_partially(database_id: str):
    pass

@router.delete("/{database_id}", status_code=204)
async def delete_database(database_id: str):
    pass

