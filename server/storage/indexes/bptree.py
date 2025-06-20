from dataclasses import dataclass, field
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
class NodeHeader:
    is_leaf: bool
    key_count: int
    parent_id: int
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'NodeHeader':
        if len(data) < 12:
            return cls(True, 0, -1)
        is_leaf, key_count, parent_id = struct.unpack('III', data)
        parent_id = parent_id if parent_id != 0xFFFFFFFF else -1
        return cls(bool(is_leaf), key_count, parent_id)
    
    def to_bytes(self) -> bytes:
        parent_id = self.parent_id if self.parent_id != -1 else 0xFFFFFFFF
        return struct.pack('III', int(self.is_leaf), self.key_count, parent_id)

@dataclass
class BPlusTreeNode:
    node_id: int
    is_leaf: bool = True
    parent_id: int = -1
    keys: list[DataType] = field(default_factory=list)
    
    def __post_init__(self):
        self.header = NodeHeader(self.is_leaf, 0, self.parent_id)
        if self.is_leaf:
            self.data_positions: list[int] = []
            self.next_leaf: int = -1
        else:
            self.pointers: list[int] = []
    
    def is_full(self, max_keys: int) -> bool:
        return len(self.keys) >= max_keys
    
    def is_underflow(self, min_keys: int) -> bool:
        return len(self.keys) < min_keys
    
    def add_record(self, record: IndexRecord) -> bool:
        if not self.is_leaf:
            return False
        
        for i, key in enumerate(self.keys):
            if key == record.key:
                self.data_positions[i] = record.position
                return True
        
        insert_pos = 0
        for i, key in enumerate(self.keys):
            if record.key < key:
                break
            insert_pos = i + 1
        
        self.keys.insert(insert_pos, record.key)
        self.data_positions.insert(insert_pos, record.position)
        self.header.key_count = len(self.keys)
        return True
    
    def remove_record(self, key: DataType) -> int | None:
        if not self.is_leaf:
            return None
        
        for i, existing_key in enumerate(self.keys):
            if existing_key == key:
                self.keys.pop(i)
                position = self.data_positions.pop(i)
                self.header.key_count = len(self.keys)
                return position
        return None
    
    def find_record(self, key: DataType) -> IndexRecord | None:
        if not self.is_leaf:
            return None
        
        for i, existing_key in enumerate(self.keys):
            if existing_key == key:
                return IndexRecord(key, self.data_positions[i])
        return None
    
    def split_leaf(self) -> tuple['BPlusTreeNode', DataType]:
        if not self.is_leaf:
            raise ValueError("Cannot split non-leaf node as leaf")
        
        mid = len(self.keys) // 2
        new_node = BPlusTreeNode(0, True, self.parent_id)
        
        # split keys and data positions
        new_node.keys = self.keys[mid:]
        new_node.data_positions = self.data_positions[mid:]
        new_node.header.key_count = len(new_node.keys)
        new_node.next_leaf = self.next_leaf
        
        # update current node
        self.keys = self.keys[:mid]
        self.data_positions = self.data_positions[:mid]
        self.header.key_count = len(self.keys)
        self.next_leaf = 0
        
        return new_node, new_node.keys[0]
    
    def split_internal(self) -> tuple['BPlusTreeNode', DataType]:
        if self.is_leaf:
            raise ValueError("Cannot split leaf node as internal")
        
        mid = len(self.keys) // 2
        promotion_key = self.keys[mid]
        
        new_node = BPlusTreeNode(0, False, self.parent_id)
        
        # split keys and pointers
        new_node.keys = self.keys[mid + 1:]
        new_node.pointers = self.pointers[mid + 1:]
        new_node.header.key_count = len(new_node.keys)
        # update current node
        self.keys = self.keys[:mid]
        self.pointers = self.pointers[:mid + 1]
        self.header.key_count = len(self.keys)
        
        return new_node, promotion_key
    
    def insert_key_internal(self, key: DataType, pointer: int):
        if self.is_leaf:
            raise ValueError("Cannot insert key into leaf node")
        
        insert_pos = 0
        for i, existing_key in enumerate(self.keys):
            if key < existing_key:
                break
            insert_pos = i + 1
        
        self.keys.insert(insert_pos, key)
        self.pointers.insert(insert_pos + 1, pointer)
        self.header.key_count = len(self.keys)
    
    def find_child_index(self, key: DataType) -> int:
        if self.is_leaf:
            return -1
        
        child_index = 0
        for i, node_key in enumerate(self.keys):
            if key < node_key:
                break
            child_index = i + 1
        
        return min(child_index, len(self.pointers) - 1)

@dataclass
class BPlusTreeHeader:
    root_node_id: int = -1
    node_count: int = 0
    height: int = 0
    record_count: int = 0
    order: int = 4
    data_type_size: int = 4
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'BPlusTreeHeader':
        if len(data) < 24:
            return cls()
        root_id, node_count, height, record_count, order, data_type_size = struct.unpack('IIIIII', data)
        root_id = root_id if root_id != 0xFFFFFFFF else -1
        return cls(root_id, node_count, height, record_count, order, data_type_size)
    
    def to_bytes(self) -> bytes:
        root_id = self.root_node_id if self.root_node_id != -1 else 0xFFFFFFFF
        return struct.pack('IIIIII', root_id, self.node_count, self.height, 
                          self.record_count, self.order, self.data_type_size)

class BPlusTreeFile(Insertable, Deletable, Updatable, Searchable):
    HEADER_SIZE = 24 # root_node_id, node_count, height, record_count, order, data_type_size
    NODE_HEADER_SIZE = 12
    
    def __init__(self, idx_filename: str, data_type: DataType, order: int = 4) -> None:
        super().__init__()
        self.idx_filename = idx_filename
        self.data_type = data_type
        self.order = order
        self.max_keys = order - 1
        self.min_keys = max(1, (order - 1) // 2)
        
        self.key_size = data_type.type_size()
        self.pointer_size = 4
        
        # use larger of internal or leaf node sizes 
        # review if this is correct
        internal_size = (self.NODE_HEADER_SIZE + 
                        (self.max_keys * self.key_size) + 
                        (self.order * self.pointer_size))
        
        leaf_size = (self.NODE_HEADER_SIZE + 
                    (self.max_keys * self.key_size) + 
                    (self.max_keys * self.pointer_size) + 
                    self.pointer_size) # next_leaf pointer
        
        self.node_size = max(internal_size, leaf_size)
        
        if os.path.getsize(idx_filename) == 0:
            self.header = BPlusTreeHeader(order=order, data_type_size=self.key_size)
            self._init_index_file()
        else:
            self._load_from_file()
    
    def insert(self, key: DataType, position: int, **args) -> bool:
        record = IndexRecord(key, position)
        
        if self.header.root_node_id == -1:
            self._create_root_leaf(record)
            return True
        
        leaf_node_id = self._find_leaf(key)
        if leaf_node_id == -1:
            return False
        
        leaf_node = self._read_node(leaf_node_id)
        
        # the key already exists? issue
        existing_record = leaf_node.find_record(key)
        if existing_record:
            leaf_node.add_record(record)
            self._write_node(leaf_node)
            return True
        
        # add new record
        leaf_node.add_record(record)
        
        if not leaf_node.is_full(self.max_keys):
            self._write_node(leaf_node)
            self.header.record_count += 1
            self._save_header()
            return True
        
        return self._handle_leaf_overflow(leaf_node)
    
    def delete(self, key: DataType) -> int | None:
        if self.header.root_node_id == -1:
            return None
        
        leaf_node_id = self._find_leaf(key)
        if leaf_node_id == -1:
            return None
        
        leaf_node = self._read_node(leaf_node_id)
        position = leaf_node.remove_record(key)
        
        if position is None:
            return None
        
        self._write_node(leaf_node)
        self.header.record_count -= 1
        self._save_header()
        
        if leaf_node.is_underflow(self.min_keys) and leaf_node_id != self.header.root_node_id:
            self._handle_underflow(leaf_node)
        
        return position
    
    def delete_all(self, key: DataType) -> any:
        return self.delete(key)
    
    def update(self, key: DataType, new_value: DataType) -> bool:
        old_value = self.delete(key)
        if old_value is None:
            return False
        return self.insert(key, new_value)
    
    def search(self, key: DataType) -> int | None:
        record = self.search_record(key)
        return record.position if record else None
    
    def search_record(self, key: DataType) -> IndexRecord | None:
        if self.header.root_node_id == -1:
            return None
        
        leaf_node_id = self._find_leaf(key)
        if leaf_node_id == -1:
            return None
        
        leaf_node = self._read_node(leaf_node_id)
        return leaf_node.find_record(key)
    
    def exist(self, key: DataType) -> bool:
        return self.search_record(key) is not None
    
    def get_all_keys(self) -> list[any]:
        keys = []
        if self.header.root_node_id == -1:
            return keys
        
        current_node_id = self._find_leftmost_leaf()
        
        while current_node_id != -1:
            node = self._read_node(current_node_id)
            for key in node.keys:
                keys.append(key.value)
            current_node_id = node.next_leaf if node.next_leaf != -1 else -1
        
        return keys
    
    def get_all_records(self) -> list[IndexRecord]:
        records = []
        if self.header.root_node_id == -1:
            return records
        
        current_node_id = self._find_leftmost_leaf()
        
        while current_node_id != -1:
            node = self._read_node(current_node_id)
            for i, key in enumerate(node.keys):
                records.append(IndexRecord(key, node.data_positions[i]))
            current_node_id = node.next_leaf if node.next_leaf != -1 else -1
        
        return records
    
    def range_search(self, start_key: DataType, end_key: DataType) -> list[IndexRecord]:
        records = []
        if self.header.root_node_id == -1:
            return records
        
        current_node_id = self._find_leaf(start_key)
        if current_node_id == -1:
            return records
        
        while current_node_id != -1:
            node = self._read_node(current_node_id)
            for i, key in enumerate(node.keys):
                if key > end_key:
                    return records
                if key >= start_key:
                    records.append(IndexRecord(key, node.data_positions[i]))
            current_node_id = node.next_leaf if node.next_leaf != -1 else -1
        
        return records
    
    def _init_index_file(self):
        with open(self.idx_filename, 'wb') as f:
            f.write(self.header.to_bytes())
    
    def _load_from_file(self):
        with open(self.idx_filename, 'rb') as f:
            header_data = f.read(self.HEADER_SIZE)
            self.header = BPlusTreeHeader.from_bytes(header_data)
            
            self.order = self.header.order
            self.max_keys = self.order - 1
            self.min_keys = max(1, (self.order - 1) // 2)
    
    def _save_header(self):
        with open(self.idx_filename, 'r+b') as f:
            f.seek(0)
            f.write(self.header.to_bytes())
    
    def _create_root_leaf(self, record: IndexRecord):
        root_node = BPlusTreeNode(0, True, -1)
        root_node.add_record(record)
        
        self.header.root_node_id = 0
        self.header.node_count = 1
        self.header.height = 1
        self.header.record_count = 1
        
        self._write_node(root_node)
        self._save_header()
    
    def _find_leaf(self, key: DataType) -> int:
        if self.header.root_node_id == -1:
            return -1
        
        current_node_id = self.header.root_node_id
        
        while current_node_id != -1:
            node = self._read_node(current_node_id)
            if node.is_leaf:
                return current_node_id
            child_index = node.find_child_index(key)

            if child_index < 0 or child_index >= len(node.pointers):
                return -1
            current_node_id = node.pointers[child_index]
        
        return -1
    
    def _find_leftmost_leaf(self) -> int:
        if self.header.root_node_id == -1:
            return -1
        
        current_node_id = self.header.root_node_id        
        while current_node_id != -1:
            node = self._read_node(current_node_id)
            if node.is_leaf:
                return current_node_id            
            if not node.pointers:
                return -1
            current_node_id = node.pointers[0]

        return -1
    
    def _handle_leaf_overflow(self, leaf_node: BPlusTreeNode) -> bool:
        new_node, promotion_key = leaf_node.split_leaf()
        
        new_node.node_id = self.header.node_count
        self.header.node_count += 1
        
        leaf_node.next_leaf = new_node.node_id
        
        self._write_node(leaf_node)
        self._write_node(new_node)
        
        self.header.record_count += 1
        self._save_header()
        
        self._insert_into_parent(leaf_node.node_id, promotion_key, new_node.node_id)
        
        return True
    
    def _insert_into_parent(self, left_child_id: int, key: DataType, right_child_id: int):
        left_node = self._read_node(left_child_id)
        
        if left_node.parent_id == -1:
            new_root = BPlusTreeNode(self.header.node_count, False, -1)
            self.header.node_count += 1
            
            new_root.keys = [key]
            new_root.pointers = [left_child_id, right_child_id]
            new_root.header.key_count = 1
            
            left_node.parent_id = new_root.node_id
            right_node = self._read_node(right_child_id)
            right_node.parent_id = new_root.node_id
            
            self.header.root_node_id = new_root.node_id
            self.header.height += 1
            
            self._write_node(new_root)
            self._write_node(left_node)
            self._write_node(right_node)
            self._save_header()
            return
        
        parent = self._read_node(left_node.parent_id)
        parent.insert_key_internal(key, right_child_id)
        
        right_node = self._read_node(right_child_id)
        right_node.parent_id = parent.node_id
        self._write_node(right_node)
        
        if parent.is_full(self.max_keys):
            self._handle_internal_overflow(parent)
        else:
            self._write_node(parent)
    
    def _handle_internal_overflow(self, internal_node: BPlusTreeNode):
        new_node, promotion_key = internal_node.split_internal()
        
        new_node.node_id = self.header.node_count
        self.header.node_count += 1
        
        # update childrens
        for pointer in new_node.pointers:
            if pointer != -1:
                child = self._read_node(pointer)
                child.parent_id = new_node.node_id
                self._write_node(child)
        
        self._write_node(internal_node)
        self._write_node(new_node)
        
        self._insert_into_parent(internal_node.node_id, promotion_key, new_node.node_id)
    
    def _handle_underflow(self, node: BPlusTreeNode):
        if node.parent_id == -1: # root node
            if node.header.key_count == 0 and not node.is_leaf and node.pointers:
                self.header.root_node_id = node.pointers[0]
                self.header.height -= 1
                new_root = self._read_node(self.header.root_node_id)
                new_root.parent_id = -1
                self._write_node(new_root)
                self._save_header()
    
    def _get_node_position(self, node_id: int) -> int:
        if node_id < 0:
            raise ValueError(f"Invalid node_id: {node_id}")
        return self.HEADER_SIZE + (node_id * self.node_size)
    
    def _read_node(self, node_id: int) -> BPlusTreeNode:
        with open(self.idx_filename, 'rb') as f:
            f.seek(self._get_node_position(node_id))
            
            header_data = f.read(self.NODE_HEADER_SIZE)
            if len(header_data) < self.NODE_HEADER_SIZE:
                raise ValueError(f"Could not read node header for node {node_id}")
            
            header = NodeHeader.from_bytes(header_data)
            
            node = BPlusTreeNode(node_id, header.is_leaf, header.parent_id)
            node.header = header
            
            for i in range(self.max_keys):
                key_data = f.read(self.key_size)
                if len(key_data) < self.key_size:
                    break
                if i < header.key_count:
                    key = self.data_type.deserialize_from_bytes(key_data)
                    node.keys.append(key)
            
            if node.is_leaf:
                for i in range(self.max_keys):
                    pos_data = f.read(self.pointer_size)
                    if len(pos_data) < self.pointer_size:
                        break
                    if i < header.key_count:
                        position = struct.unpack('I', pos_data)[0]
                        node.data_positions.append(position)
                
                next_data = f.read(self.pointer_size)
                if len(next_data) >= self.pointer_size:
                    next_leaf = struct.unpack('I', next_data)[0]
                    node.next_leaf = next_leaf if next_leaf != 0xFFFFFFFF else -1
            else:
                for i in range(self.order):
                    ptr_data = f.read(self.pointer_size)
                    if len(ptr_data) < self.pointer_size:
                        break
                    if i <= header.key_count:
                        pointer = struct.unpack('I', ptr_data)[0]
                        node.pointers.append(pointer)
            
            return node
    
    def _write_node(self, node: BPlusTreeNode):
        required_size = self._get_node_position(node.node_id) + self.node_size
        current_size = os.path.getsize(self.idx_filename)
        
        if required_size > current_size:
            with open(self.idx_filename, 'ab') as f:
                f.write(b'\0' * (required_size - current_size))
        
        with open(self.idx_filename, 'r+b') as f:
            f.seek(self._get_node_position(node.node_id))
            
            f.write(node.header.to_bytes())
            
            for i in range(self.max_keys):
                if i < len(node.keys):
                    key_data = self.data_type.serialize_to_bytes(node.keys[i])
                else:
                    key_data = b'\0' * self.key_size
                f.write(key_data)
            
            if node.is_leaf:
                for i in range(self.max_keys):
                    if i < len(node.data_positions):
                        f.write(struct.pack('I', node.data_positions[i]))
                    else:
                        f.write(struct.pack('I', 0))
                
                next_leaf = node.next_leaf if node.next_leaf != -1 else 0xFFFFFFFF
                f.write(struct.pack('I', next_leaf))
            else:
                for i in range(self.order):
                    if i < len(node.pointers):
                        f.write(struct.pack('I', node.pointers[i]))
                    else:
                        f.write(struct.pack('I', 0))
            
            current_pos = f.tell()
            expected_pos = self._get_node_position(node.node_id) + self.node_size
            if current_pos < expected_pos:
                f.write(b'\0' * (expected_pos - current_pos))