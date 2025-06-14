from typing import Annotated
from fastapi import Depends
from pathlib import Path

from server.engine.executor import PinPom
from server.catalog.database import DatabaseService
from server.catalog.catalog import CatalogService

# Depends
def get_pinpom() -> PinPom:
    base_path = Path("data")
    return PinPom(base_path=base_path)

def get_catalog_service(pinpom: PinPom = Depends(get_pinpom)) -> CatalogService:
    return pinpom.catalog_service

def get_database_service(pinpom: PinPom = Depends(get_pinpom)) -> DatabaseService:
    return pinpom.database_service

# Type hints
DatabaseServiceDep = Annotated[DatabaseService, Depends(get_database_service)]