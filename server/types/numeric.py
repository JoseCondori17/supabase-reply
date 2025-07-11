import struct
from server.types.base import DataType

class SmallIntType(DataType[int]):
    def compare(self, other: 'SmallIntType') -> int:
        if self.value < other.value:
            return -1
        elif self.value > other.value:
            return 1
        return 0
    
    def serialize(self) -> dict[str, any]:
        return {
            "type": "smallint",
            "value": self.value
        }
    
    def serialize_to_bytes(self) -> bytes:
        format_str = self.type_format()
        return struct.pack(format_str, self.value)

    def type_size(self) -> int:
        return 2

    def type_format(self) -> str:
        return 'h'
    
    @classmethod
    def deserialize(cls, data: dict[str, any]) -> 'SmallIntType':
        if data["type"] != "smallint":
            raise ValueError("Invalid type for SmallInt")
        return cls(data["value"])
    
    @classmethod
    def deserialize_from_bytes(cls, data: bytes, **args) -> 'SmallIntType':
        if len(data) != 2:
            raise ValueError("Invalid data size for SmallInt")
        value = struct.unpack('h', data)[0]
        return cls(value)

class IntType(DataType[int]):
    def compare(self, other: 'IntType') -> int:
        if self.value < other.value:
            return -1
        elif self.value > other.value:
            return 1
        return 0
    
    def serialize(self) -> dict[str, any]:
        return {
            "type": "int",
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
    def deserialize(cls, data: dict[str, any]) -> 'IntType':
        if data["type"] != "int":
            raise ValueError("Invalid type for Int")
        if data["value"] is None:
            return cls(0)
        return cls(int(data["value"]))
    
    @classmethod
    def deserialize_from_bytes(cls, data: bytes, **args) -> 'IntType':
        if len(data) != 4:
            raise ValueError("Invalid data size for Int")
        value = struct.unpack('i', data)[0]
        return cls(value)

class BigIntType(DataType[int]):
    def compare(self, other: 'BigIntType') -> int:
        if self.value < other.value:
            return -1
        elif self.value > other.value:
            return 1
        return 0
    
    def serialize(self) -> dict[str, any]:
        return {
            "type": "bigint",
            "value": self.value
        }
    
    def serialize_to_bytes(self) -> bytes:
        format_str = self.type_format()
        return struct.pack(format_str, self.value)

    def type_size(self) -> int:
        return 8

    def type_format(self) -> str:
        return 'q'
    
    @classmethod
    def deserialize(cls, data: dict[str, any]) -> 'BigIntType':
        if data["type"] != "bigint":
            raise ValueError("Invalid type for BigInt")
        if data["value"] is None:
            return cls(0)
        return cls(int(data["value"]))
    
    @classmethod
    def deserialize_from_bytes(cls, data: bytes, **args) -> 'BigIntType':
        if len(data) != 8:
            raise ValueError("Invalid data size for BigInt")
        value = struct.unpack('q', data)[0]
        return cls(value)

IntegerType = IntType # alias for compatibility with existing code

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
        return 'd'
    
    @classmethod
    def deserialize(cls, data: dict[str, any]) -> 'FloatType':
        if data["type"] != "float":
            raise ValueError("Invalid type for FloatType")
        if data["value"] is None:
            return cls(float(0))
        return cls(float(data["value"]))
    
    @classmethod
    def deserialize_from_bytes(cls, data: bytes, **args) -> 'FloatType':
        if len(data) != 8:
            raise ValueError("Invalid data size for FloatType")
        value = struct.unpack('d', data)[0]
        return cls(value)