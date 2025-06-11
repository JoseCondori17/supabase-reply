from dataclasses import dataclass

from server.catalog.service import BaseService
from server.storage.disk.file_manager import FileManager
from server.storage.disk.path_builder import PathBuilder


@dataclass
class Column(BaseService):
    att_name        : str
    att_type_id     : int
    att_len         : int
    att_not_null    : bool
    att_has_def     : bool
    
class ColumnService(BaseService):
    def __init__(self, file_manager: FileManager, path_builder: PathBuilder):
        super().__init__(file_manager, path_builder)