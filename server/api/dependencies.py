from typing import Annotated
from fastapi import Depends
from server.engine.executor import PinPom
from server.api.v1.dependencies import get_pinpom, get_database_service, DatabaseServiceDep

# global var
admin_instance: PinPom | None = None

def get_pinpom() -> PinPom:
    if admin_instance is None:
        raise RuntimeError("PinPom instance not initialized")
    return admin_instance

PinPomDep = Annotated[PinPom, Depends(get_pinpom)]

# dependencies
__all__ = ['get_pinpom', 'get_database_service', 'DatabaseServiceDep']