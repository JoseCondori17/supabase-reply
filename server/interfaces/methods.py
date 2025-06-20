from typing import Protocol, Iterator, Literal
from server.types.base import DataType

class Insertable(Protocol):
    def insert(self, key: DataType, position: int, **args): ...

class Searchable(Protocol):
    def search(self, key: DataType) -> DataType: ... # only value
    def search_record(self, key: DataType) -> DataType: ... # all record
    def exist(self, key: DataType) -> bool: ...
    
class Deletable(Protocol):
    def delete(self, key: DataType) -> DataType: ...
    def delete_all(self, key: DataType) -> DataType: ...
    
class Updatable(Protocol):
    def update(self, key: DataType, new_key: DataType) -> bool: ...
    
class RangeSearchable(Protocol):
    def range_search(self, range_query) -> DataType: ...
    def range_count(self, start_key: DataType, end_key: DataType) -> int: ...
    
class FullTextSearchable(Protocol):
    def search_text(self, text: str, limit: int | None = None) -> DataType: ...
    def search_prefix(self, prefix: str, limit: int | None = None) -> DataType: ...
    
class Iterable(Protocol):
    def get_all_keys(self) -> list[DataType]: ...
    def get_all_records(self) -> list[DataType]: ...
    def keys(self) -> Iterator[DataType]: ...
    def values(self) -> Iterator[DataType]: ...
    def items(self) -> Iterator[tuple[DataType, DataType]]: ...
    
class Sortable(Protocol):
    def get_sorted_keys(self, order: Literal["ASC", "DESC"], limit: int | None = None): ...
    def get_sorted_records(self, order = Literal["ASC", "DESC"], limit: int | None = None): ...
    