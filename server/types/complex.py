import json
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
    
    @classmethod
    def deserialize(cls, data: dict) -> 'JSONType':
        return cls(json.loads(data['value']))

class GeometricType(DataType[dict[str, any]]):
    def compare(self, other: 'GeometricType') -> int:
        if self.value == other.value:
            return 0
        return -1
    
    def serialize(self) -> dict:
        return {
            'type': 'GEOMETRIC',
            'value': self.value
        }
    
    @classmethod
    def deserialize(cls, data: dict) -> 'GeometricType':
        return cls(data['value']) 