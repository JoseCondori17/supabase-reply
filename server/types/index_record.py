from dataclasses import dataclass
from server.types.base import DataType

@dataclass
class IndexRecord:
    key: DataType
    position: int
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, IndexRecord):
            return self.key == other.key
        return False