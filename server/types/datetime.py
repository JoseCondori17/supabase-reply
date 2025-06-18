from datetime import datetime, date, time
import struct
from server.types.base import DataType

class DateType(DataType[date]):
    def compare(self, other: 'DateType') -> int:
        if self.value < other.value:
            return -1
        if self.value > other.value:
            return 1
        return 0
    
    def serialize(self) -> dict:
        return {
            'type': 'DATE',
            'value': self.value.isoformat()
        }
    
    def serialize_to_bytes(self) -> bytes:
        format_str = self.type_format()
        return struct.pack(format_str, self.value.isoformat().encode('utf-8'))
    
    def type_size(self) -> int:
        return 10

    def type_format(self) -> str:
        return '10s'
    
    @classmethod
    def deserialize(cls, data: dict) -> 'DateType':
        return cls(date.fromisoformat(data['value']))
    
    @classmethod
    def deserialize_from_bytes(cls, data: bytes) -> DataType:
        if len(data) != 10:
            raise ValueError("Invalid data size for DateType")
        value = struct.unpack('10s', data)[0].decode('utf-8').strip()
        return cls(date.fromisoformat(value))

class TimeType(DataType[time]):
    def compare(self, other: 'TimeType') -> int:
        if self.value < other.value:
            return -1
        if self.value > other.value:
            return 1
        return 0
    
    def serialize(self) -> dict:
        return {
            'type': 'TIME',
            'value': self.value.isoformat()
        }
    
    def serialize_to_bytes(self) -> bytes:
        format_str = self.type_format()
        return struct.pack(format_str, self.value.isoformat().encode('utf-8'))

    def type_size(self) -> int:
        return 8
    
    def type_format(self) -> str:
        return '8s'
    
    @classmethod
    def deserialize(cls, data: dict) -> 'TimeType':
        return cls(time.fromisoformat(data['value']))
    
    @classmethod
    def deserialize_from_bytes(cls, data: bytes) -> DataType:
        if len(data) != 8:
            raise ValueError("Invalid data size for TimeType")
        value = struct.unpack('8s', data)[0].decode('utf-8').strip()
        return cls(time.fromisoformat(value))

class TimestampType(DataType[datetime]):
    def compare(self, other: 'TimestampType') -> int:
        if self.value < other.value:
            return -1
        if self.value > other.value:
            return 1
        return 0
    
    def serialize(self) -> dict:
        return {
            'type': 'TIMESTAMP',
            'value': self.value.isoformat()
        }
    
    def serialize_to_bytes(self) -> bytes:
        format_str = self.type_format()
        return struct.pack(format_str, self.value.isoformat().encode('utf-8'))

    def type_size(self) -> int:
        return 26

    def type_format(self) -> str:
        return '26s'  # YYYY-MM-DD HH:MM:SS.mmmmmm
    
    @classmethod
    def deserialize(cls, data: dict) -> 'TimestampType':
        return cls(datetime.fromisoformat(data['value'])) 
    
    @classmethod
    def deserialize_from_bytes(cls, data: bytes) -> DataType:
        if len(data) != 26:
            raise ValueError("Invalid data size for TimestampType")
        value = struct.unpack('26s', data)[0].decode('utf-8').strip()
        return cls(datetime.fromisoformat(value))