from abc import ABC, abstractmethod
from typing import TypeVar, Generic
# I prefer use future from bindings - review 12/06

T = TypeVar('T')

class DataType(Generic[T], ABC):

    def __init__(self, value: T):
        self._value = value
    
    @property
    def value(self) -> T:
        return self._value
    
    @abstractmethod
    def compare(self, other: 'DataType[T]') -> int: pass
    
    @abstractmethod
    def serialize(self) -> dict: pass
    
    @abstractmethod
    def serialize_to_bytes(self) -> bytes: pass

    @abstractmethod
    def type_size(self) -> int: pass
    
    @abstractmethod
    def type_format(self) -> str: pass
    
    @classmethod
    @abstractmethod
    def deserialize(cls, data: dict) -> 'DataType[T]': pass

    @classmethod
    @abstractmethod
    def deserialize_from_bytes(cls, data: bytes) -> 'DataType[T]': pass
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.compare(other) == 0
    
    def __lt__(self, other: 'DataType[T]') -> bool:
        return self.compare(other) < 0
    
    def __gt__(self, other: 'DataType[T]') -> bool:
        return self.compare(other) > 0
    
    def __le__(self, other: 'DataType[T]') -> bool:
        return self.compare(other) <= 0
    
    def __ge__(self, other: 'DataType[T]') -> bool:
        return self.compare(other) >= 0 