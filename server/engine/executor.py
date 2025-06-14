from pathlib import Path
from dataclasses import dataclass, field
from sqlglot.expressions import *

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

    def __post_init__(self):
        self.catalog_service = CatalogService(self.file_manager, self.path_builder, self.base_path)
        self.database_service = DatabaseService(self.file_manager, self.path_builder, self.catalog_service)
        self.schema_service = SchemaService(self.file_manager, self.path_builder, self.database_service)
        self.table_service = TableService(self.file_manager, self.path_builder, self.schema_service)
        self.database_global: str = "ppsql"
        self.schema_global: str = "public"

    def execute(self, sql: str) -> None:
        exprs = self.sql_parser.parse(sql)
        results = []
        
        for expr in exprs:
            try:
                if isinstance(expr, Create):
                    result = self.create_op(expr)
                elif isinstance(expr, Drop):
                    result = self.drop_op(expr)
                elif isinstance(expr, Select):
                    result = self.select_op(expr)
                elif isinstance(expr, Insert):
                    result = self.insert_op(expr)
                elif isinstance(expr, Delete):
                    result = self.delete_op(expr)
                else:
                    raise ValueError(f"Operation not supported: {type(expr)}")
                
                if result is not None:
                    results.append(result)
                    
            except Exception as e:
                print(f"Error in building: {str(e)}")
                continue
                
        return results

    def drop_op(self, expr: Expression):
        if expr.kind == "TABLE":
            parser = self.sql_parser._parse_drop_table(expr)
        elif expr.kind == "DATABASE":
            parser = self.sql_parser._parse_drop_database(expr)
        elif expr.kind == "SCHEMA":
            parser = self.sql_parser._parse_drop_schema(expr)
    def create_op(self, expr: Expression):
        if expr.kind == "TABLE":
            parser = self.sql_parser._parse_create_table(expr)
            self.table_service.create_table(
                db_name=self.database_global,
                sch_name=self.schema_global,
                tab_name=parser['name'],
                columns=parser['columns']
            )
            return
        if expr.kind == "DATABASE":
            parser = self.sql_parser._parse_create_database(expr)
            db_name = parser['name']
            self.database_service.create_database(db_name)
            self.database_global = db_name
            return
        if expr.kind == "SCHEMA":
            parser = self.sql_parser._parse_create_schema(expr)
            sch_name = parser['name']
            self.schema_service.create_schema(
                db_name=self.database_global,
                sch_name=sch_name
            )
            self.schema_global = sch_name
            return
        if expr.kind == "INDEX":
            parser = self.sql_parser._parse_create_index(expr)
            return
    def select_op(self, expr: Expression):
        parser = self.sql_parser._parse_select_from(expr)
    def delete_op(self, expr: Expression):
        parser = self.sql_parser._parse_delete_from_table(expr)
    def insert_op(self, expr: Expression):
        parser = self.sql_parser._parse_insert_into_values(expr)
        
    def set_database(self, db_name) -> None:
        self.database = db_name
    def set_schema(self, schema_name) -> None:
        self.schema = schema_name
    