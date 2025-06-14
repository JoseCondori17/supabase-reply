from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import TYPE_CHECKING

from server.catalog.service import BaseService
from server.storage.disk.file_manager import FileManager
from server.storage.disk.path_builder import PathBuilder
from server.catalog.column import Column
from server.catalog.index import Index

if TYPE_CHECKING:
    from server.catalog.schema import SchemaService
    

@dataclass
class Table:
    tab_id          : int
    tab_name        : str
    tab_namespace   : int  # schema id
    tab_tuples      : int  # quantity of records
    tab_columns     : list[Column] = field(default_factory=list)
    tab_indexes     : list[Index] = field(default_factory=list)

class TableService(BaseService):
    def __init__(self, file_manager: FileManager, path_builder: PathBuilder, schema_service: 'SchemaService'):
        super().__init__(file_manager, path_builder)
        self.schema_service = schema_service
    
    def create_table(self, db_name: str, sch_name: str, tab_name: str, columns: list[Column]) -> bool:
        schema = self.schema_service.get_schema(db_name, sch_name)
        if tab_name in schema.sch_tables.keys():
            print(f"Table '{db_name}' already exists")
            return False
        
        table_paths = self._create_table_structure(db_name, sch_name, tab_name)
        table_id = self._generate_table_id(schema)
        table_namespace = schema.get_id()
        table_tuples = 0
        table = Table(
            table_id,
            tab_name,
            table_namespace,
            table_tuples,
            columns,
            []
        )
        schema.sch_tables[tab_name] = table_id # add table
        self.schema_service._update_schema_metadata(db_name, sch_name, schema)
        
        self.file_manager.write_data(table, table_paths['meta'])

        return True

    def get_table(self, db_name: str, sch_name: str, tab_name: str) -> Table:
        table_meta_path = self.path_builder.table_meta(db_name, sch_name, tab_name)
        return self.file_manager.read_data(table_meta_path)
    
    def get_table_json(self, db_name: str, sch_name: str, tab_name: str) -> dict[Table]:
        table_meta_path = self.path_builder.table_meta(db_name, sch_name, tab_name)
        table = self.file_manager.read_data(table_meta_path)
        return asdict(table)

    def get_tables(self, db_name: str, sch_name: str) -> list[Table]:
        schema = self.schema_service.get_schema(db_name, sch_name)
        tables = []
        for table_name in schema.sch_tables.keys():
            tables.append(self.get_table(db_name, sch_name, table_name))
        return tables
    
    def get_tables_json(self, db_name: str, sch_name: str) -> list[dict[Table]]:
        schema = self.schema_service.get_schema(db_name, sch_name)
        tables = []
        for table_name in schema.sch_tables.keys():
            table = self.get_table(db_name, sch_name, table_name)
            tables.append(asdict(table))
        return tables
    
    def get_tables_name(self, db_name: str, sch_name: str) -> list[str]:
        return [table.tab_name for table in self.get_tables(db_name, sch_name)]
    
    def _generate_table_id(self, db_name: str, sch_name: str):
        schema = self.schema_service.get_schema(db_name, sch_name)
        return max(schema.sch_tables.values(), default=0) + 1
    
    def _create_table_structure(self, db_name: str, schema_name: str, table_name: str) -> dict[str, Path]:
        paths = {
            'table': self.path_builder.table_dir(db_name, schema_name, table_name),
            'data': self.path_builder.table_data(db_name, schema_name, table_name),
            'meta': self.path_builder.table_meta(db_name, schema_name, table_name)
        }
        
        self._ensure_directory_exists(paths['table'])
        self._ensure_file_exists(paths['data'])
        self._ensure_file_exists(paths['meta'])
        
        return paths