from typing import Type
from server.types.base import DataType
from server.types.numeric import IntegerType, FloatType, BigIntType, IntType, SmallIntType
from server.types.text import StringType, TextType
from server.types.datetime import DateType, TimeType, TimestampType
from server.types.special import UUIDType, BooleanType
from server.types.complex import JSONType, GeometricType

class TypeFactory:
    
    _type_registry: dict[str, Type[DataType]] = {
        # numerics
        "smallint": SmallIntType,
        "integer": IntegerType,
        "int": IntType,
        "bigint": BigIntType,
        "double": FloatType,
        # "decimal": DecimalType,
        
        # text
        "char": StringType,
        "varchar": StringType,
        "text": TextType,
        
        # date
        "date": DateType,
        "time": TimeType,
        "timestamp": TimestampType,
        
        # special
        "uuid": UUIDType,
        "boolean": BooleanType,
        
        # complex
        "json": JSONType,
        "geometric": GeometricType
    }
    
    @classmethod
    def create(cls, type_name: str, value: any) -> DataType:
        if type_name not in cls._type_registry:
            raise ValueError(f"Unknown type: {type_name}")
        
        return cls._type_registry[type_name](value)
    
    @classmethod
    def from_dict(cls, data: dict[str, any]) -> DataType:
        if "type" not in data:
            raise ValueError("Missing 'type' in data")
        
        type_name = data["type"]
        if type_name not in cls._type_registry:
            raise ValueError(f"Unknown type: {type_name}")
        
        return cls._type_registry[type_name].deserialize(data)
    
    @classmethod
    def register_type(cls, type_name: str, type_class: Type[DataType]) -> None:
        cls._type_registry[type_name] = type_class 