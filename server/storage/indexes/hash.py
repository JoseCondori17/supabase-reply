from dataclasses import dataclass, field
from xxhash import xxh64
import struct
import os

from server.types.base import DataType
from server.types.index_record import IndexRecord
from server.interfaces.methods import (
    Insertable, 
    Deletable, 
    Updatable, 
    Searchable
)

@dataclass
class BucketHeader:
    local_depth: int
    max_size: int
    record_count: int
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'BucketHeader':
        if len(data) < 12: return cls(0, 0, 0)
        local_depth, max_size, record_count = struct.unpack('III', data)
        return cls(local_depth, max_size, record_count)
    def to_bytes(self) -> bytes:
        return struct.pack('III', self.local_depth, self.max_size, self.record_count)

@dataclass
class Bucket:
    bucket_id: int
    local_depth: int = 0
    max_size: int = 0
    records: list[IndexRecord] = field(default_factory=[])
    
    def __post_init__(self):
        self.header = BucketHeader(self.local_depth, self.max_size, 0)
    
    def is_full(self) -> bool:
        return len(self.records) >= self.header.max_size
    
    def add_record(self, record: IndexRecord) -> bool:
        for i, exist_record in enumerate(self.records):
            if exist_record.key == record.key:
                self.records[i] = record
                return True
        
        if self.is_full(): return False
        
        self.records.append(record)
        self.header.record_count = len(self.records)
        return True
    
    def remove_record(self, key: DataType) -> bool:
        for i, record in enumerate(self.records):
            if record.key == key:
                self.records.pop(i)
                self.header.record_count = len(self.records)
                return True
        return False
    
    def find_record(self, key: DataType) -> IndexRecord | None:
        for record in self.records:
            if record.key == key:
                return record
        return None
    
    def split_record(self, bit_position: int, hash_function: callable) -> tuple[list[IndexRecord], list[IndexRecord]]:
        bucket_1 = []
        bucket_2 = []
        
        for record in self.records:
            hash_value = hash_function(record.key)
            if self._get_bit(hash_value, bit_position):
                bucket_2.append(record)
            else:
                bucket_1.append(record)
        return bucket_1, bucket_2
                
    def _get_bit(self, number:int, position: int) -> bool:
        return bool((number >> position) & 1)
        
@dataclass
class Directory:
    global_depth: int = 0
    
    def __post_init__(self):
        self.size = 1 << self.global_depth # 2¨global
        self.entries: list = field(default_factory=[0] * self.size)
        
    def get_bucket_id(self, hash_value) -> int:
        mask = (1 << self.global_depth) - 1
        index = hash_value & mask
        return self.entries[index]
    
    def expand(self): # duplicate
        old_entries = self.entries.copy()
        self.global_depth += 1
        self.size = 1 << self.global_depth
        
        self.entries = [
            old_entries[i % len(old_entries)]
            for i in range(self.size)
        ]
        
    def update_after_split(self, old_bucket_id: int, new_bucket_id: int, local_depth: int):
        high_bit = 1 << (local_depth - 1)
        
        for i in range(len(self.entries)):
            if self.entries[i] == old_bucket_id and (i & high_bit):
                self.entries[i] = new_bucket_id

@dataclass
class IndexHeader:
    global_depth: int = 0
    directory_size: int = 1
    bucket_count: int = 1
    header_size: int = 12 # global, dir size, bucket count
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'IndexHeader':
        global_depth, directory_size, bucket_count = struct.unpack('III', data)
        return cls(global_depth, directory_size, bucket_count)
    
    def to_bytes(self) -> bytes:
        return struct.pack('III', self.global_depth, self.directory_size, self.bucket_count)

class ExtendibleHashingFile(Insertable, Deletable, Updatable, Searchable):
    DIRECTORY_ENTRY_SIZE = 4 # 4 bit for each entry(int)
    
    def __init__(self, idx_filename: str, data_type: DataType, bucket_size: int = 10) -> None:
        super().__init__()
        self.idx_filename = idx_filename
        self.bucket_size = bucket_size
        self.data_type = data_type
        
        if os.path.getsize(idx_filename) == 0:
            self.header = IndexHeader()
            self.directory = Directory()
            self._init_index_file()
        else:
            self._laod_from_file()
          
    def insert(self, key: DataType, value: any, **args) -> bool: ...
    def delete(self, key: DataType) -> any: ...
    def delete_all(self, key: DataType) -> any: ...
    def update(self, key: DataType) -> bool: ...
    def get_all_keys(self) -> list[DataType]: ...
    def get_all_records(self) -> list[IndexRecord]: ...
    def search(self, key: DataType) -> int: ...
    def search_record(self, key: DataType) -> IndexRecord: ...
    def exist(self, key: DataType) -> bool: ...
    
    def _init_index_file(self):
       with open(self.idx_filename, 'wb') as f:
            f.write(self.header.to_bytes())
            for bucket_id in self.directory.entries:
                f.write(struct.pack('I', bucket_id))
                empty_bucket = Bucket(0, 0, self.bucket_size)
                # write bucket
                
    def _laod_from_file(self):
        with open(self.idx_filename, 'rb') as f:
            header_data = f.read(IndexHeader.header_size)
            self.header = IndexHeader.from_bytes(header_data)
            
            self.directory = Directory(self.header.global_depth)
            for i in range(self.header.directory_size):
                bucket_id = struct.unpack('I', f.read(4))[0]
                self.directory.entries[i] = bucket_id
                
    def _get_bucket_position(self):
        directory_size = self.directory.size * 4
        return 
    
    
    def _read_bucket(self, bucket_id: int) -> Bucket:
        with open(self.idx_filename, 'rb') as f:
            pass
 
    def hash_function(self, key: DataType):
        key_bytes = key.type_format()
        if isinstance(key.value, str):
            key_bytes = key.type_format(len(key.value))
        
        return xxh64(key_bytes).intdigest()
