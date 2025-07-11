from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from server.catalog.service import BaseService
from server.catalog.database import Database
from server.storage.disk.file_manager import FileManager
from server.storage.disk.path_builder import PathBuilder

@dataclass
class Catalog:
    databases: dict[str, Database] = field(default_factory=dict[str, Database])
    version: str = field(default="0.0.1")
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

class CatalogService(BaseService):
    def __init__(self, file_manager: FileManager, path_builder: PathBuilder, data_directory: Path):
        super().__init__(file_manager, path_builder)
        self.data_directory = data_directory
        self.system_catalog_path = data_directory / Path("system/catalog.dat")
        self.catalog = Catalog()
        self.initialize_catalog()

    def initialize_catalog(self) -> None:
        if self.file_manager.path_exists(self.system_catalog_path):
            self.load_catalog()
        else:
            self.save_catalog()

    def load_catalog(self) -> Catalog:
        self.catalog: Catalog = self.file_manager.read_data(self.system_catalog_path)
        return self.catalog
    
    def save_catalog(self) -> None:
        if self.catalog is None:
            raise ValueError("No catalog to save")
        
        self._ensure_file_exists(self.system_catalog_path)
        self.file_manager.write_data(self.catalog, self.system_catalog_path)
    
    def get_version(self) -> str:
        return self.catalog.version
    
    def get_created_at(self) -> datetime:
        return self.catalog.created_at
    
    def get_databases(self) -> dict[str, Database]:
        return self.catalog.databases