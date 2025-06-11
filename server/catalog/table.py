from dataclasses import dataclass, field, asdict

from server.catalog.service import BaseService
from server.catalog.schema import SchemaService, Schema
from server.storage.disk.file_manager import FileManager
from server.storage.disk.path_builder import PathBuilder
from catalog.column import Column
from catalog.index import Index

@dataclass
class Table:
    tab_id          : int
    tab_name        : str
    tab_namespace   : int  # schema id
    tab_tuples      : int  # quantity of records
    tab_pages       : int  # number of pages
    tab_page_size   : int  # size of page
    tab_columns     : list[Column] = field(default_factory=list)
    tab_indexes     : list[Index] = field(default_factory=list)

class TableService(BaseService):
    def __init__(self, file_manager: FileManager, path_builder: PathBuilder, schema_service: SchemaService):
        super().__init__(file_manager, path_builder)
        self.schema_service = schema_service
    
    # https://claude.ai/chat/6edafe21-ccfe-4d55-9159-e5f54a7ff729
    # pending
    def create_table(self, db_name: str, sch_name: str, tab_name: str, columns: list[Column]) -> bool:
        schema = self.schema_service.get_schema(db_name, sch_name)
        if tab_name in schema.sch_tables.keys():
            print(f"Table '{db_name}' already exists")
            return False
        
        table_path = self._create_table_structure(db_name, sch_name, tab_name)
        table_id = self._generate_table_id(schema)
        table = Table(
            table_id,
            tab_name,
            schema.get_id(),
            0,
            1,
            8192,
            columns,
            []
        )
        schema.add_table(tab_name, table_id)
        self.schema_service._update_schema_metadata(db_name, sch_name, schema)

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
        for table_name in schema.get_tables().keys():
            tables.append(self.get_table(db_name, sch_name, table_name))
        return tables
    
    def get_tables_json(self, db_name: str, sch_name: str) -> list[dict[Table]]:
        schema = self.schema_service.get_schema(db_name, sch_name)
        tables = []
        for table_name in schema.get_tables().keys():
            table = self.get_table(db_name, sch_name, table_name)
            tables.append(asdict(table))
        return tables
    
    def get_tables_name(self, db_name: str, sch_name: str) -> list[str]:
        return [table.get_tab_name() for table in self.get_tables(db_name, sch_name)]