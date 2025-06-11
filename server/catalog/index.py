from dataclasses import dataclass, asdict
from pathlib import Path

from server.catalog.service import BaseService
from server.catalog.table import TableService
from server.storage.disk.file_manager import FileManager
from server.storage.disk.path_builder import PathBuilder

@dataclass
class Index:
    idx_id          : int
    idx_type        : int
    idx_name        : str
    idx_file        : Path
    idx_tuples      : int
    idx_columns     : list[int]  # column positions
    idx_is_primary  : bool
    
class IndexService(TableService):
    def __init__(self, file_manager: FileManager, path_builder: PathBuilder, table_service: TableService):
        super().__init__(file_manager, path_builder)
        self.table_service = table_service
    
    def get_index(self, db_name: str, sch_name: str, tab_name: str, idx_name: str) -> Index | None:
        table = self.table_service.get_table(db_name, sch_name, tab_name)
        for index in table.tab_indexes:
            if index.idx_name == idx_name:
                return index
        return None

    def get_index_json(self, db_name: str, sch_name: str, tab_name: str, idx_name: str) -> dict[Index]:
        table = self.table_service.get_table(db_name, sch_name, tab_name)
        for index in table.tab_indexes:
            if index.idx_name == idx_name:
                return asdict(index)
        return {}
    
    def get_indexes(self, db_name: str, sch_name: str, tab_name: str) -> list[Index]:
        table = self.table_service.get_table(db_name, sch_name, tab_name)
        return table.tab_indexes
        
    def get_indexes_json(self, db_name: str, sch_name: str, tab_name: str) -> list[dict[Index]]:
        table = self.table_service.get_table(db_name, sch_name, tab_name)
        indexes_json = [asdict(index) for index in table.tab_indexes]
        return indexes_json
    
    def get_indexes_name(self, db_name: str, sch_name: str, tab_name) -> list[str]:
        table = self.table_service.get_table(db_name, sch_name, tab_name)
        indexes_name = [index.idx_name for index in table.tab_indexes]
        return indexes_name

    def _generate_index_id(self, db_name: str, sch_name: str, tab_name):
        table = self.table_service.get_table(db_name, sch_name, tab_name)
        indexes_id = [index.idx_id for index in table.tab_indexes]
        return max(indexes_id, default=0) + 1
    