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
            self._load_from_file()
          
    def insert(self, key: DataType, position: int, **args) -> bool:
        record = IndexRecord(key, position)
        hash_value = self.hash_function(key)
        bucket_id = self.directory.get_bucket_id(hash_value)

        bucket = self._read_bucket(bucket_id)
        if bucket.add_record(record):
            self._write_bucket(bucket)
            return True
        return self._handle_bucket_overflow(bucket, record)

    def delete(self, key: DataType) -> int | None:
        hash_value = self.hash_function(key)
        bucket_id = self.directory.get_bucket_id(hash_value)
        bucket = self._read_bucket(bucket_id)

        record = bucket.find_record(key)
        if record is None:
            return None
        
        if bucket.remove_record(key):
            self._write_bucket(bucket)
            return record.position
        
        return None

    def delete_all(self, key: DataType) -> any: ...

    def update(self, key: DataType, new_value: DataType) -> bool:
        old_value = self.delete(key)
        if old_value is None:
            return False
        return self.insert(key, new_value)
    
    def get_all_keys(self) -> list[int]: # review return
        keys = []
        for bucket_id in range(self.header.bucket_count):
            bucket = self._read_bucket(bucket_id)
            for record in bucket.records:
                if record.key.value not in keys:
                    keys.append(record.key.value)
        return keys
    
    def get_all_records(self) -> list[IndexRecord]:
        keys = []
        for bucket_id in range(self.header.bucket_count):
            bucket = self._read_bucket(bucket_id)
            for record in bucket.records:
                if record.key not in keys:
                    keys.append(record.key)
        return keys
    
    def search(self, key: DataType) -> int:
        record = self.search_record(key)
        return record.position if record else None
    
    def search_record(self, key: DataType) -> IndexRecord:
        hash_value = self.hash_function(key)
        bucket_id = self.directory.get_bucket_id(hash_value)
        bucket = self._read_bucket(bucket_id)
        return bucket.find_record(key)
    
    def exist(self, key: DataType) -> bool:
        return self.search_record(key) is not None
    
    def _init_index_file(self):
       with open(self.idx_filename, 'wb') as f:
            f.write(self.header.to_bytes()) # write main header
            for bucket_id in self.directory.entries:
                f.write(struct.pack('I', bucket_id))

            empty_bucket = Bucket(0, 0, self.bucket_size)
            self._write_bucket_to_file(f, empty_bucket)
                
    def _load_from_file(self):
        with open(self.idx_filename, 'rb') as f:
            header_data = f.read(IndexHeader.header_size)
            self.header = IndexHeader.from_bytes(header_data)
            
            self.directory = Directory(self.header.global_depth)
            for i in range(self.header.directory_size):
                bucket_id = struct.unpack('I', f.read(4))[0]
                self.directory.entries[i] = bucket_id

    def _handle_bucket_overflow(self, bucket: Bucket, new_record: IndexRecord) -> bool:
        if bucket.local_depth == self.directory.global_depth:
            self.directory.expand()
            self.header.global_depth = self.directory.global_depth
            self.header.directory_size = self.directory.size        
        return self._split_bucket(bucket, new_record) # split bucket

    def _split_bucket(self, bucket: Bucket, new_record: IndexRecord) -> bool:
        bucket.records.append(new_record)
        # update detpth
        new_local_depth = bucket.local_depth + 1
        bit_position = bucket.local_depth
        # split records- using 'class Bucket'
        records_1, records_2 = bucket.split_records(bit_position, self.hash_function)
        # new bucket
        new_bucket_id = self.header.bucket_count
        self.header.bucket_count += 1
        # update bucket
        bucket.records = records_1
        bucket.local_depth = new_local_depth
        bucket.header.record_count = len(records_1)
        bucket.header.local_depth = new_local_depth
        
        # create new bucket and update directory: used Directory class
        # [...data] original
        # [...data] new
        new_bucket = Bucket(new_bucket_id, new_local_depth, self.bucket_size, records_2)
        self.directory.update_after_split(bucket.bucket_id, new_bucket_id, new_local_depth)

        self._write_bucket(bucket)
        self._write_bucket(new_bucket)
        
        self._save_header()
        self._save_directory()

    def _get_bucket_position(self, bucket_id: int) -> int:
        header_size = 12  # main header
        directory_size = self.header.directory_size * 4  # 4 b for each entries
        bucket_header_size = 12  # local depth, max size, record count
        record_size = self.data_type.type_size() + 4  # size of key (value) + position
        bucket_size = bucket_header_size + (self.bucket_size * record_size)
        return header_size + directory_size + (bucket_id * bucket_size)
    
    def _read_bucket(self, bucket_id: int) -> Bucket:
        with open(self.idx_filename, 'rb') as f:
            position = self._get_bucket_position(bucket_id)
            f.seek(position)
            header_data = f.read(12)
            if len(header_data) < 12:
                return Bucket(bucket_id, 0, self.bucket_size)
            bucket_header = BucketHeader.from_bytes(header_data)
            records = []
            for _ in range(bucket_header.record_count):
                key_data = f.read(self.data_type.type_size())
                position_data = f.read(4)
                
                if len(key_data) < self.data_type.type_size() or len(position_data) < 4:
                    break
                
                position = struct.unpack('I', position_data)[0]
                key = self.data_type.deserialize_from_bytes(key_data)
                records.append(IndexRecord(key, position))
            
            return Bucket(bucket_id, bucket_header.local_depth, bucket_header.max_size, records)

    def _write_bucket(self, bucket: Bucket):
        with open(self.idx_filename, 'r+b') as f:
            position = self._get_bucket_position(bucket.bucket_id)
            f.seek(position)
            self._write_bucket_to_file(f, bucket)

    def _write_bucket_to_file(self, f, bucket: Bucket):
        f.write(bucket.header.to_bytes())
        # write records [*max_size of bucket]
        for record in bucket.records:
            key_data = self.data_type.serialize_to_bytes(record.key)
            f.write(key_data)
            f.write(struct.pack('I', record.position))

    def _save_header(self):
        with open(self.idx_filename, 'r+b') as f:
            f.seek(0)
            f.write(self.header.to_bytes())

    def _save_directory(self):
        with open(self.idx_filename, 'r+b') as f:
            f.seek(12) # after header
            for bucket_id in self.directory.entries:
                f.write(struct.pack('I', bucket_id))

    def hash_function(self, key: DataType): # review this
        key_bytes = struct.pack(key.type_format(), key.value)
        return xxh64(key_bytes).intdigest()
