from datetime import datetime, date, time
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
    
    def type_format(self, size: int | None = None) -> str:
        return '10s'
    
    @classmethod
    def deserialize(cls, data: dict) -> 'DateType':
        return cls(date.fromisoformat(data['value']))

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
    
    def type_format(self, size: int | None = None) -> str:
        return '8s'
    
    @classmethod
    def deserialize(cls, data: dict) -> 'TimeType':
        return cls(time.fromisoformat(data['value']))

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
    
    def type_format(self, size: int | None = None) -> str:
        return '26s'  # YYYY-MM-DD HH:MM:SS.mmmmmm
    
    @classmethod
    def deserialize(cls, data: dict) -> 'TimestampType':
        return cls(datetime.fromisoformat(data['value'])) 