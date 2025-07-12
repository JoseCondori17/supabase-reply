from fastapi import APIRouter, HTTPException

from server.api.v1.dependencies import PinPomDep
from server.api.v1.model.query import Query

router = APIRouter()

@router.post("/sql", status_code=201)
async def query_sql(pp_service: PinPomDep, body: Query):
    try:
        result = pp_service.execute(body.query)
        return {
            "success": True,
            "data": result
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