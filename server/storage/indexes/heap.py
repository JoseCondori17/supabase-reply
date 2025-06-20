from dataclasses import dataclass
from typing import overload

from server.interfaces.methods import Insertable, Deletable, Updatable, Searchable
from server.types.base import DataType
from server.enums.data_type_enum import DataTypeLabel
from server.catalog.column import Column, ColumnService

@dataclass
class HeapFile:
    heap_filename: str
    columns: list[Column]
    
    def insert(self, values: list[DataType]) -> int:
        with open(self.heap_filename, 'a+b') as f:
            values_bin = b''.join(value.serialize_to_bytes() for value in values)
            f.write(values_bin)
            f.flush()
            offset = f.tell()
            values_size = sum(value.type_size() for value in values)
            return offset / values_size

    def delete(self, key: DataType) -> any: ...
    def delete_all(self, key: DataType) -> any: ...
    def update(self, key: DataType, new_key: DataType) -> bool: ...
    
    def get_record(self, selection: list[str], conditions: list[dict]) -> list[DataType]:
        with open(self.heap_filename, 'rb') as f:
            row = self.get_row(f, self.columns)

            if len(selection) == 0 or selection[0] == '*':
                return row
            else:
                return [row[i] for i, col in enumerate(self.columns) if col.att_name in selection]
            
    def get_record_by_position(self, position: int) -> list[DataType]:
        with open(self.heap_filename, 'rb') as f:
            total_size = sum(col.att_len for col in self.columns)
            f.seek(position * total_size)
            
            return [
                ColumnService.deserialize_from_bytes(col.att_type_id, f.read(col.att_len), type_size=col.att_len)
                for col in self.columns
            ]
        
    def get_all_keys(self) -> list[DataType]: ...
    def get_all_records(self, selection: list[str], conditions: list[dict] = None) -> list[DataType]:
        records = []
        with open(self.heap_filename, 'rb') as f:
            while True:
                try:
                    row = self.get_row(f, self.columns)
                    if selection[0] == '*':
                        records.append(row)
                    else:
                        filtered_row = [row[i] for i, col in enumerate(self.columns) if col.att_name in selection]
                        records.append(filtered_row)
                except EOFError:
                    break
        return records
            

    def search(self, key: DataType) -> int: ...
    def search_record(self, key: DataType) -> DataType: ...
    def exist(self, key: DataType) -> bool: ...

    # tools
    def get_row(self, f, columns: list[Column]) -> list[DataType]:
        values = []
        for col in self.columns:
            data = f.read(col.att_len)
            if not data:  # break or if data is None:
                raise EOFError("End of file reached")
            value = ColumnService.desearialize_from_bytes(col.att_type_id, data[:col.att_len], type_size=col.att_len)
            values.append(value)
        return values