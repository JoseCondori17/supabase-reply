from server.types.base import DataType

class StringType(DataType[str]):
    def compare(self, other: 'StringType') -> int:
        if self.value < other.value:
            return -1
        elif self.value > other.value:
            return 1
        return 0
    
    def serialize(self) -> dict[str, any]:
        return {
            "type": "string",
            "value": self.value
        }
    
    @classmethod
    def deserialize(cls, data: dict[str, any]) -> 'StringType':
        if data["type"] != "string":
            raise ValueError("Invalid type for StringType")
        return cls(data["value"])

class TextType(DataType[str]):
    def compare(self, other: 'TextType') -> int:
        if self.value < other.value:
            return -1
        elif self.value > other.value:
            return 1
        return 0
    
    def serialize(self) -> dict[str, any]:
        return {
            "type": "text",
            "value": self.value
        }
    
    @classmethod
    def deserialize(cls, data: dict[str, any]) -> 'TextType':
        if data["type"] != "text":
            raise ValueError("Invalid type for TextType")
        return cls(data["value"]) 