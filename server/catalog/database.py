from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import TYPE_CHECKING


from server.catalog.service import BaseService
from server.storage.disk.file_manager import FileManager
from server.storage.disk.path_builder import PathBuilder

if TYPE_CHECKING:
    from server.catalog.catalog import CatalogService
    
@dataclass
class Database:
    db_id           : int
    db_name         : str
    db_schemas      : dict[str, int] = field(default_factory=dict)
    db_created_at   : datetime = field(default_factory=lambda: datetime.now(timezone.utc))

class DatabaseService(BaseService):
    def __init__(self, file_manager: FileManager, path_builder: PathBuilder, catalog_service: 'CatalogService'):
        super().__init__(file_manager, path_builder)
        self.catalog_service = catalog_service

    def create_database(self, db_name: str) -> bool:
        catalog = self.catalog_service.catalog
        if db_name in catalog.databases.keys():
            print(f"Database '{db_name}' already exists")
            return False
        
        db_path = self.path_builder.database_dir(db_name)
        db_meta_path = self.path_builder.database_meta(db_name)

        self.file_manager.create_dir(db_path)
        self.file_manager.create_file(db_meta_path)

        db_id = self._generate_database_id()
        database = Database(db_id, db_name)

        catalog.databases[db_name] = database
        self.catalog_service.save_catalog()
        return True

    def get_database(self, db_name: str) -> Database | None:
        catalog = self.catalog_service.catalog
        database = catalog.databases.get(db_name)
        return database

    def get_database_json(self, db_name: str) -> dict[Database]:
        catalog = self.catalog_service.catalog
        database = catalog.databases.get(db_name)
        return asdict(database)
    
    def get_databases(self) -> list[Database]:
        catalog = self.catalog_service.catalog
        databases = [db for db in catalog.databases.values()]
        return databases

    def get_databases_json(self) -> list[dict[Database]]:
        catalog = self.catalog_service.catalog
        databases = [asdict(db) for db in catalog.databases.values()]
        return databases
    
    def get_databases_name(self) -> list[str]:
        catalog = self.catalog_service.catalog
        databases = [db.db_name for db in catalog.databases.values()]
        return databases
    
    def _generate_database_id(self) -> int:
        databases_id = [db.db_id for db in self.get_databases()]
        return max(databases_id, default=0) + 1
    
    def _update_database_metadata(self, db_name: str, database: Database) -> None:
        db_meta_path = self.path_builder.database_meta(db_name)
        self.file_manager.write_data(database, db_meta_path)