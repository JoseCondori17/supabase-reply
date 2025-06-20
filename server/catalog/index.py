from dataclasses import dataclass, asdict
from pathlib import Path
from typing import TYPE_CHECKING

from server.catalog.service import BaseService
from server.catalog.column import ColumnService
from server.storage.disk.file_manager import FileManager
from server.storage.disk.path_builder import PathBuilder
from server.enums.index_enum import IndexTypeLabel

from server.storage.indexes.hash import ExtendibleHashingFile
from server.storage.indexes.bptree import BPlusTreeFile

if TYPE_CHECKING:
    from server.catalog.table import TableService

@dataclass
class Index:
    idx_id          : int
    idx_type        : int
    idx_name        : str
    idx_file        : Path
    idx_tuples      : int
    idx_columns     : list[int]  # column positions
    idx_is_primary  : bool
    

# pending: add primary key support dynamically
class IndexService(BaseService):
    _indexes = {
        "sequential": BPlusTreeFile,
        "avl": BPlusTreeFile,
        "isam": BPlusTreeFile,
        "hash": ExtendibleHashingFile, # check
        "btree": BPlusTreeFile, # check
        "rtree": BPlusTreeFile,
    }

    def __init__(self, file_manager: FileManager, path_builder: PathBuilder, table_service: 'TableService'):
        super().__init__(file_manager, path_builder)
        self.table_service = table_service
    
    def create_index(self, 
                     db_name: str, 
                     sch_name: str, 
                     tab_name: str, 
                     idx_name: str, 
                     idx_type: str, 
                     idx_column: str, 
                     idx_is_primary: bool = False
        ) -> Index: 
        table = self.table_service.get_table(db_name, sch_name, tab_name)
        idx_id = self._generate_index_id(db_name, sch_name, tab_name)
        idx_file = self.path_builder.table_index(db_name, sch_name, tab_name, idx_name)
        idx_columns = [i for i, tab in enumerate(table.tab_columns) if tab.att_name == idx_column]

        index = Index(
            idx_id=idx_id,
            idx_type=IndexTypeLabel[idx_type.upper()].value,
            idx_name=idx_name,
            idx_file=idx_file,
            idx_tuples=0,
            idx_columns=idx_columns,
            idx_is_primary=idx_is_primary
        )
        
        table.tab_indexes.append(index)
        self.table_service._update_table(db_name, sch_name, table)
        self._ensure_file_exists(idx_file)
        return index

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
    
    @classmethod
    def call_indexes(cls, indexes: list[Index], columns: list):
        # pending: change to use index type enum
        callables_fn = []
        for index in indexes:
            index_type = IndexTypeLabel(index.idx_type).name.lower()
            if index_type not in cls._indexes:
                continue
            else:
                column_pos = index.idx_columns[0]
                column_info = columns[column_pos]
                data_type_instance = ColumnService.to_type(column_info.att_type_id, None, type_size=column_info.att_len) 
                index_file = index.idx_file
                if index_type == "hash":
                    index = {
                        'index': ExtendibleHashingFile(index_file, data_type_instance, bucket_size=10),
                        'column_index': column_pos,
                    }
                    callables_fn.append(index)
                elif index_type == "btree":
                    index = {
                        'index': BPlusTreeFile(index_file, data_type_instance, order=5),
                        'column_index': column_pos,
                    }
                    callables_fn.append(index)
                elif index_type == "isam":
                    pass
                elif index_type == "avl":
                    pass
                elif index_type == "rtree":
                    pass
        return callables_fn