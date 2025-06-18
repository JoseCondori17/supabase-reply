import uuid
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
            'type': 'UUID',
            'value': str(self.value)
        }
    
    def type_format(self, size: int | None = None) -> str:
        # UUID string length (8-4-4-4-12 format)
        # ref: https://feasiblecommerce.com/index.php/home/blog/blog-uuid
        return '36s'
    
    @classmethod
    def deserialize(cls, data: dict) -> 'UUIDType':
        return cls(uuid.UUID(data['value']))

class BooleanType(DataType[bool]):
    def compare(self, other: 'BooleanType') -> int:
        if self.value == other.value:
            return 0
        return -1 if not self.value else 1
    
    def serialize(self) -> dict:
        return {
            'type': 'BOOLEAN',
            'value': self.value
        }
    
    def type_format(self, size: int | None = None) -> str:
        return '?'
    
    @classmethod
    def deserialize(cls, data: dict) -> 'BooleanType':
        return cls(bool(data['value'])) 