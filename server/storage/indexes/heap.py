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
            return int(offset / values_size)

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
        
    def get_record_json(self, selection: list[str], conditions: list[dict]) -> dict:
        record = self.get_record(selection, conditions)
        return {col.att_name: record[i] for i, col in enumerate(self.columns) if col.att_name in selection}

    def get_record_by_position(self, position: int) -> list[DataType]:
        with open(self.heap_filename, 'rb') as f:
            total_size = sum(col.att_len for col in self.columns)
            f.seek(position * total_size)
            
            return [
                ColumnService.deserialize_from_bytes(col.att_type_id, f.read(col.att_len), type_size=col.att_len)
                for col in self.columns
            ]

    def get_all_records_json(self, selection: list[str], limit: int = None, conditions: list[dict] = None) -> list[dict]:
        records = []
        count = 0
        with open(self.heap_filename, 'rb') as f:
            while True:
                try:
                    row = self.get_row_json(f, self.columns)
                    if not conditions or self.evaluate_condition(conditions, row):
                        if selection[0] == '*':
                            records.append(row)
                        else:
                            filtered_row = {
                                col.att_name: row[col.att_name].value
                                for col in self.columns if col.att_name in selection
                            }
                            records.append(filtered_row)

                        count += 1
                        if limit is not None and count >= limit:
                            break
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
    
    def get_row_json(self, f, columns: list[Column]) -> dict:
        row = self.get_row(f, columns)
        return {col.att_name: row[i] for i, col in enumerate(columns)}

    def evaluate_condition(self, node, data) -> bool:
        node_type = node['type']
        
        if node_type in ('AND', 'OR'):
            left_result = self.evaluate_condition(node['left'], data)
            if node_type == 'AND' and not left_result:
                return False
            if node_type == 'OR' and left_result:
                return True
            right_result = self.evaluate_condition(node['right'], data)
            return left_result and right_result if node_type == 'AND' else left_result or right_result
        
        # BASIC OPERATORS
        elif node_type in ('LT', 'LTE', 'GT', 'GTE', 'EQ', 'NEQ'):
            column_value = data.get(node['column'])
            if column_value is None:
                raise KeyError(f"Column '{node['column']}' not found")
            
            if node_type == 'LT':
                return column_value < node['value']
            elif node_type == 'LTE':
                return column_value <= node['value']
            elif node_type == 'GT':
                return column_value > node['value']
            elif node_type == 'GTE':
                return column_value >= node['value']
            elif node_type == 'EQ':
                return column_value == node['value']
            elif node_type == 'NEQ':
                return column_value != node['value']
        
        # BETWEEN
        elif node_type == 'BETWEEN':
            column_value = data.get(node['column'])
            if column_value is None:
                raise KeyError(f"Column '{node['column']}' not found")
            return node['low'] <= column_value <= node['high']
        
        # COSENO <->
        elif node_type == 'COSENO':
            column_value = data.get(node['column'])
            if column_value is None:
                raise KeyError(f"Column '{node['column']}' not found")
            
        # MANHAT <#>
        elif node_type == 'MANHATAN':
            column_value = data.get(node['column'])
            if column_value is None:
                raise KeyError(f"Column '{node['column']}' not found")
            
        # LINEAL <=>
        elif node_type == 'LINEAL':
            column_value = data.get(node['column'])
            if column_value is None:
                raise KeyError(f"Column '{node['column']}' not found")
            
        else:
            raise ValueError(f"Operator not support: {node_type}")
        