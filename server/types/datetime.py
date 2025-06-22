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
            'type': 'date',
            'value': self.value.isoformat()
        }
    
    def serialize_to_bytes(self) -> bytes:
        format_str = self.type_format()
        return struct.pack(format_str, self.value.year, self.value.month, self.value.day)
    
    def type_size(self) -> int:
        return 4

    def type_format(self) -> str:
        return '!HBB'
    
    @classmethod
    def deserialize(cls, data: dict) -> 'DateType':
        return cls(date.fromisoformat(data['value']))
    
    @classmethod
    def deserialize_from_bytes(cls, data: bytes, **args) -> 'DateType':
        if len(data) != 4:
            raise ValueError("Invalid data size for DateType")
        year, month, day = struct.unpack('!HBB', data)
        return cls(date(year, month, day))

class TimeType(DataType[time]):
    def compare(self, other: 'TimeType') -> int:
        if self.value < other.value:
            return -1
        if self.value > other.value:
            return 1
        return 0
    
    def serialize(self) -> dict:
        return {
            'type': 'time',
            'value': self.value.isoformat()
        }
    
    def serialize_to_bytes(self) -> bytes:
        format_str = self.type_format()
        return struct.pack(format_str, 
                          self.value.hour, 
                          self.value.minute, 
                          self.value.second,
                          self.value.microsecond)

    def type_size(self) -> int:
        return 5
    
    def type_format(self) -> str:
        return '!BBBH'
    
    @classmethod
    def deserialize(cls, data: dict) -> 'TimeType':
        return cls(time.fromisoformat(data['value']))
    
    @classmethod
    def deserialize_from_bytes(cls, data: bytes, **args) -> 'TimeType':
        if len(data) != 5:
            raise ValueError("Invalid data size for TimeType")
        h, m, s, ms = struct.unpack('!BBBH', data)
        return cls(time(h, m, s, ms))

class TimestampType(DataType[datetime]):    
    def compare(self, other: 'TimestampType') -> int:
        if self.value < other.value:
            return -1
        if self.value > other.value:
            return 1
        return 0
    
    def serialize(self) -> dict:
        return {
            'type': 'timestamp',
            'value': self.value.isoformat()
        }
    
    def serialize_to_bytes(self) -> bytes:
        format_str = self.type_format()
        timestamp = int(self.value.timestamp() * 1_000_000)
        return struct.pack(format_str, timestamp)

    def type_size(self) -> int:
        return 8

    def type_format(self) -> str:
        return '!Q'  # unix timestamp in microseconds
    
    @classmethod
    def deserialize(cls, data: dict) -> 'TimestampType':
        return cls(datetime.fromisoformat(data['value'])) 
    
    @classmethod
    def deserialize_from_bytes(cls, data: bytes, **args) -> 'TimestampType':
        if len(data) != 8:
            raise ValueError("Invalid data size for TimestampType")
        microseconds = struct.unpack('!Q', data)[0]
        return cls(datetime.fromtimestamp(microseconds / 1_000_000))