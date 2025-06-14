from dataclasses import dataclass, field, asdict

from server.catalog.service import BaseService
from server.catalog.database import DatabaseService
from server.storage.disk.file_manager import FileManager
from server.storage.disk.path_builder import PathBuilder

@dataclass
class Schema:
    sch_id          : int
    sch_name        : str
    sch_db_id       : int
    sch_tables      : dict[str, int] = field(default_factory=dict)
    sch_functions   : dict[str, int] = field(default_factory=dict)

class SchemaService(BaseService):
    def __init__(self, file_manager: FileManager, path_builder: PathBuilder, database_service: DatabaseService):
        super().__init__(file_manager, path_builder)
        self.database_service = database_service

    def create_schema(self, db_name: str, sch_name: str) -> bool:
        database = self.database_service.get_database(db_name)
        if sch_name in database.db_schemas.keys():
            print(f"Schema '{sch_name}' already exists")
            return False
        
        schema_path = self.path_builder.schema_dir(db_name, sch_name)
        schema_meta_path = self.path_builder.schema_meta(db_name, sch_name)
        
        self._ensure_directory_exists(schema_path)
        self._ensure_file_exists(schema_meta_path)

        schema_id = self._generate_schema_id(database)
        schema = Schema(schema_id, sch_name, database.db_id)

        database.db_schemas[sch_name] = schema_id
        self.database_service._update_database_metadata(db_name, database)

        self.file_manager.write_data(schema, schema_meta_path)
        self.database_service.catalog_service.save_catalog()
        
        return True

    def get_schema(self, db_name: str, sch_name: str) -> Schema:
        schema_meta_path = self.path_builder.schema_meta(db_name, sch_name)
        schema: Schema = self.file_manager.read_data(schema_meta_path)
        return schema

    def get_schema_json(self, db_name: str, sch_name: str) -> dict[Schema]:
        schema_meta_path = self.path_builder.schema_meta(db_name, sch_name)
        schema: Schema = self.file_manager.read_data(schema_meta_path)
        return asdict(schema)
    
    def get_schemas(self, db_name: str) -> list[Schema]:
        database = self.database_service.get_database(db_name)
        schemas = []
        for schema_name in database.db_schemas.keys():
            schemas.append(self.get_schema(db_name, schema_name))
        return schemas
    
    def get_schemas_json(self, db_name: str) -> list[dict[Schema]]:
        database = self.database_service.get_database(db_name)
        schemas_str = [schema for schema in database.db_schemas.keys()]
        schemas = []
        for item in schemas_str:
            schema_meta_path = self.path_builder.schema_meta(db_name, item)
            schema: Schema = self.file_manager.read_data(schema_meta_path)
            schemas.append(asdict(schema))
        return schemas
    
    def get_schemas_name(self, db_name: str) -> list[str]:
        database = self.database_service.get_database(db_name)
        schemas = [schema_name for schema_name in database.db_schemas.keys()]
        return schemas

    def _generate_schema_id(self, db_name: str) -> int:
        database = self.database_service.get_database(db_name)
        return max(database.db_schemas.values(), default=0) + 1
    
    def _update_schema_metadata(self, db_name: str, schema_name: str, schema: Schema) -> None:
        schema_meta_path = self.path_builder.schema_meta(db_name, schema_name)
        self.file_manager.write_data(schema, schema_meta_path)