from abc import ABC, abstractmethod
from typing import TypeVar, Generic
# check

T = TypeVar('T')

class DataType(Generic[T], ABC):

    def __init__(self, value: T, size: int = None):
        self._value = value
        self.size = size if size is not None else self.type_size()
    
    @property
    def value(self) -> T:
        return self._value
    
    @property
    def class_type(self) -> str:
        return self.__class__.__name__

    @property    
    def type(self) -> str:
        return self.class_type.lower().removesuffix('type')
    
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
    def deserialize_from_bytes(cls, data: bytes, **args) -> 'DataType[T]': pass
    
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