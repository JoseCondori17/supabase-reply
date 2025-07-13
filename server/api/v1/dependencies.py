from typing import Annotated
from fastapi import Depends
from pathlib import Path

from server.engine.executor import PinPom
from server.catalog.catalog import CatalogService
from server.catalog.database import DatabaseService
from server.catalog.schema import SchemaService
from server.catalog.table import TableService
from server.utils.scripts.subset_context import switch_subset

# singleton instance
_pinpom_instance: PinPom | None = None

def get_pinpom() -> PinPom:
    global _pinpom_instance
    if _pinpom_instance is None:
        base_path = Path("data")
        _pinpom_instance = PinPom(base_path=base_path)
    return _pinpom_instance

def get_catalog_service(pinpom: PinPom = Depends(get_pinpom)) -> CatalogService:
    return pinpom.catalog_service

def get_database_service(pinpom: PinPom = Depends(get_pinpom)) -> DatabaseService:
    return pinpom.database_service

def get_schema_service(pinpom: PinPom = Depends(get_pinpom)) -> SchemaService:
    return pinpom.schema_service

def get_table_service(pinpom: PinPom = Depends(get_pinpom)) -> TableService:
    return pinpom.table_service
def switch_and_reload(subset_size: int):
    global _pinpom_instance
    switch_subset(subset_size)   # cambia la ruta / contexto
    base_path = Path("data")
    _pinpom_instance = PinPom(base_path=base_path)  # se vuelve a crear

# type hints
PinPomDep = Annotated[PinPom, Depends(get_pinpom)]
DatabaseServiceDep = Annotated[DatabaseService, Depends(get_database_service)]
SchemaServiceDep = Annotated[SchemaService, Depends(get_schema_service)]
TableServiceDep = Annotated[TableService, Depends(get_table_service)]