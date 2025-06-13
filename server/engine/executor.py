from pathlib import Path
from dataclasses import dataclass, field

from server.sql.sql_parser import SQLParser
from server.storage.disk.file_manager import FileManager
from server.storage.disk.path_builder import PathBuilder

from server.catalog.catalog import CatalogService
from server.catalog.database import DatabaseService
from server.catalog.schema import SchemaService
from server.catalog.table import TableService

@dataclass
class PinPom:
    base_path: Path = Path("data")
    file_manager: FileManager = field(default_factory=lambda: FileManager(Path("data")))
    path_builder: PathBuilder = field(default_factory=lambda: PathBuilder(Path("data")))
    sql_parser: SQLParser = field(default_factory=lambda: SQLParser())

    def __post_ini__(self):
        self.catalog_service = CatalogService(self.file_manager, self.path_builder, self.base_path)
        self.database_service = DatabaseService(self.file_manager, self.path_builder, self.catalog_service)
        self.schema_service = SchemaService(self.file_manager, self.path_builder, self.database_service)
        self.table_service = TableService(self.file_manager, self.path_builder, self.schema_service)

    def execute(self, sql: str):
        parsed = self.sql_parser.parse(sql)
        # add condition for types of query