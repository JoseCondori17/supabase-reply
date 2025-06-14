from typing import Annotated
from fastapi import Depends
from server.engine.executor import PinPom

# global var
admin_instance: PinPom | None = None

def get_pinpom() -> PinPom:
    if admin_instance is None:
        raise RuntimeError("PinPom instance not initialized")
    return admin_instance

PinPomDep = Annotated[PinPom, Depends(get_pinpom)]