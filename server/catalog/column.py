from dataclasses import dataclass

from server.catalog.service import BaseService
from server.storage.disk.file_manager import FileManager
from server.storage.disk.path_builder import PathBuilder

from server.enums.data_type_enum import DataTypeLabel
from server.types.factory import TypeFactory

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

    @classmethod
    def to_type(cls, type_id: int, value: any, type_size: int = None):
        type_name = DataTypeLabel(type_id).name.lower()
        if type_name in ["string", "varchar", "char"] and type_size is not None:
            return TypeFactory.from_dict({'type': type_name, 'value': value, 'size': type_size})
        return TypeFactory.from_dict({'type': type_name, 'value': value})
    
    @classmethod
    def desearialize_from_bytes(cls, type_id: int, value: bytes, type_size: int = None):
        type_name = DataTypeLabel(type_id).name.lower()
        return TypeFactory._type_registry[type_name].deserialize_from_bytes(value, type_size=type_size)