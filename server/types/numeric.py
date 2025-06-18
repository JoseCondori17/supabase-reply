import struct
from server.types.base import DataType

class IntegerType(DataType[int]):
    def compare(self, other: 'IntegerType') -> int:
        if self.value < other.value:
            return -1
        elif self.value > other.value:
            return 1
        return 0
    
    def serialize(self) -> dict[str, any]:
        return {
            "type": "integer",
            "value": self.value
        }
    
    def serialize_to_bytes(self) -> bytes:
        format_str = self.type_format()
        return struct.pack(format_str, self.value)

    def type_size(self) -> int:
        return 4

    def type_format(self) -> str:
        return 'i'
    
    @classmethod
    def deserialize(cls, data: dict[str, any]) -> 'IntegerType':
        if data["type"] != "integer":
            raise ValueError("Invalid type for IntegerType")
        return cls(data["value"])
    
    @classmethod
    def deserialize_from_bytes(cls, data: bytes) -> DataType:
        if len(data) != 4:
            raise ValueError("Invalid data size for IntegerType")
        value = struct.unpack('i', data)[0]
        return cls(value)

class FloatType(DataType[float]):
    def compare(self, other: 'FloatType') -> int:
        if self.value < other.value:
            return -1
        elif self.value > other.value:
            return 1
        return 0
    
    def serialize(self) -> dict[str, any]:
        return {
            "type": "float",
            "value": self.value
        }
    
    def serialize_to_bytes(self) -> bytes:
        format_str = self.type_format()
        return struct.pack(format_str, self.value)

    def type_size(self) -> int:
        return 8
    
    def type_format(self) -> str:
        return 'f'
    
    @classmethod
    def deserialize(cls, data: dict[str, any]) -> 'FloatType':
        if data["type"] != "float":
            raise ValueError("Invalid type for FloatType")
        return cls(data["value"])
    
    @classmethod
    def deserialize_from_bytes(cls, data: bytes) -> DataType:
        if len(data) != 8:
            raise ValueError("Invalid data size for FloatType")
        value = struct.unpack('f', data)[0]
        return cls(value)