import uuid
import struct
from server.types.base import DataType

class UUIDType(DataType[uuid.UUID]):
    def compare(self, other: 'UUIDType') -> int:
        if self.value < other.value:
            return -1
        if self.value > other.value:
            return 1
        return 0
    
    def serialize(self) -> dict:
        return {
            'type': 'uuid',
            'value': str(self.value)
        }
    
    def serialize_to_bytes(self) -> bytes:
        format_str = self.type_format()
        return struct.pack(format_str, str(self.value).encode('utf-8'))

    def type_size(self) -> int:
        return 36

    def type_format(self) -> str:
        # UUID string length (8-4-4-4-12 format)
        # ref: https://feasiblecommerce.com/index.php/home/blog/blog-uuid
        return '36s'
    
    @classmethod
    def deserialize(cls, data: dict) -> 'UUIDType':
        return cls(uuid.UUID(data['value']))
    
    @classmethod
    def deserialize_from_bytes(cls, data: bytes, **args) -> 'UUIDType':
        if len(data) != 36:
            raise ValueError("Invalid data size for UUIDType")
        value = struct.unpack('36s', data)[0].decode('utf-8').strip()
        return cls(uuid.UUID(value))

class BooleanType(DataType[bool]):
    def compare(self, other: 'BooleanType') -> int:
        if self.value == other.value:
            return 0
        return -1 if not self.value else 1
    
    def serialize(self) -> dict:
        return {
            'type': 'boolean',
            'value': self.value
        }
    
    def serialize_to_bytes(self) -> bytes:
        format_str = self.type_format()
        return struct.pack(format_str, self.value)
    
    def type_size(self) -> int:
        return 1

    def type_format(self) -> str:
        return '?'
    
    @classmethod
    def deserialize(cls, data: dict) -> 'BooleanType':
        return cls(bool(data['value'])) 
    
    @classmethod
    def deserialize_from_bytes(cls, data: bytes, **args) -> 'BooleanType':
        if len(data) != 1:
            raise ValueError("Invalid data size for BooleanType")
        value = struct.unpack('?', data)[0]
        return cls(value)