from fastapi import APIRouter, Query
from server.engine.executor import PinPom
from server.storage.indexes.inverted_index import InvertedIndex

router = APIRouter()

@router.post("/", status_code=200)
async def search(query: str = Query(...), top_k: int = Query(5)):
    db = "mi_db"
    schema = "mi_schema"
    table = "mi_tabla"
    column = "mi_campo"

    # Construye PinPom para rutas
    pinpom = PinPom()
    index = InvertedIndex(pinpom.file_manager, pinpom.path_builder, db, schema, table, column)

    results = index.query(query, top_k=top_k)
    return {"results": results}
