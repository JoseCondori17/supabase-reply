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
    
    @classmethod
    def deserialize(cls, data: dict[str, any]) -> 'IntegerType':
        if data["type"] != "integer":
            raise ValueError("Invalid type for IntegerType")
        return cls(data["value"])

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
    
    @classmethod
    def deserialize(cls, data: dict[str, any]) -> 'FloatType':
        if data["type"] != "float":
            raise ValueError("Invalid type for FloatType")
        return cls(data["value"])
    