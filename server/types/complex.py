import json
import struct
from server.types.base import DataType

class JSONType(DataType[dict[str, any]]):
    def compare(self, other: 'JSONType') -> int:
        if self.value == other.value:
            return 0
        return -1
    
    def serialize(self) -> dict:
        return {
            'type': 'JSON',
            'value': json.dumps(self.value)
        }
    
    def serialize_to_bytes(self) -> bytes:
        format_str = self.type_format()
        json_str = json.dumps(self.value)
        return struct.pack(format_str, json_str.encode('utf-8'))

    def type_size(self) -> int:
        return len(json.dumps(self.value).encode('utf-8'))

    def type_format(self) -> str:
        size = self.type_size()
        if size <= 0:
            raise ValueError("JSONType requires a size parameter")
        return f'{size}s'
    
    @classmethod
    def deserialize(cls, data: dict) -> 'JSONType':
        return cls(json.loads(data['value']))
    
    @classmethod
    def deserialize_from_bytes(cls, data: bytes) -> DataType:
        if len(data) <= 0:
            raise ValueError("Invalid data size for JSONType")
        format_str = f'{len(data)}s'
        value = struct.unpack(format_str, data)[0].decode('utf-8').strip()
        return cls(json.loads(value))

# review: define the type or format for geometric data
class GeometricType(DataType[dict[str, any]]):
    def compare(self, other: 'GeometricType') -> int:
        if self.value == other.value:
            return 0
        return -1
    
    def serialize(self) -> dict:
        return {
            'type': 'GEOMETRIC',
            'value': json.dumps(self.value)
        }
    
    def serialize_to_bytes(self) -> bytes:
        format_str = self.type_format()
        json_str = json.dumps(self.value)
        return struct.pack(format_str, json_str.encode('utf-8'))
    
    def type_size(self) -> int:
        return len(json.dumps(self.value).encode('utf-8'))

    def type_format(self) -> str:
        size = self.type_size()
        if size <= 0:
            raise ValueError("GeometricType requires a size parameter")
        return f'{size}s'
    
    @classmethod
    def deserialize(cls, data: dict) -> 'GeometricType':
        return cls(json.loads(data['value']))
    
    @classmethod
    def deserialize_from_bytes(cls, data: bytes) -> DataType:
        if len(data) <= 0:
            raise ValueError("Invalid data size for GeometricType")
        format_str = f'{len(data)}s'
        value = struct.unpack(format_str, data)[0].decode('utf-8').strip()
        return cls(json.loads(value))
    