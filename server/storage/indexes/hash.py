#from xxhash import xxh64
import struct
import os

from server.storage.indexes.types.interfaces import Insertable, Deletable, Iterable, Updatable, Searchable

class ExtendibleHashingFile(Insertable, Deletable, Updatable, Searchable):
    HEADER_SIZE = 12 # global_depth + directory_size + bucket_count
    DIRECTORY_ENTRY_SIZE = 4 
    BUCKET_HEADER_SIZE = 12 # local_depth + max_size + record_count
    
    def __init__(self, idx_filename: str, data_type, key_len: int, bucket_size: int = 10) -> None:
        self.idx_filename = idx_filename
        self.data_type = data_type
        self.key_len = key_len
        self.bucket_size = bucket_size
        
        self.global_depth = 0
        self.directory_size = 1
        self.bucket_count = 1
        
        if self._is_file_empty():
            self._initialize_index_file()
        else:
            self._load_header()
        
    def insert(self, key: any, value: any, **args) -> bool:
        pass
        
    def delete(self, key: any) -> any:
        pass
        
    def delete_all(self, key: any) -> any:
        pass
        
    def update(self, key: any) -> bool:
        pass
        
    def get_all_keys(self) -> list[any]:
        pass
        
    def get_all_records(self) -> list[any]:
        pass
    def search(self, key: any) -> any: 
        ...
    def search_record(self, key: any) -> any: 
        ...
    def exist(self, key: any) -> bool: 
        ...
        
    def _initialize_index_file(self):
        with open(self.idx_filename, 'wb') as f:
            data = struct.pack('III', self.global_depth, self.directory_size, self.bucket_count)
            f.write(data)
            f.write(struct.pack('I', 0))
            self._write_bucket_at_position()
    def _load_header(self): ...
    def _save_header(self): ...
    def _is_file_empty(self): ...
    
    def _read_directory(): ...
    def _write_directory(): ...
    def _write_bucket_at_position(): ...
    def _write_bucket(): ...
    def _get_bucket_by_position(): ...
    def _hash_key(): ...
    def _get_bucket_index(): ...
    