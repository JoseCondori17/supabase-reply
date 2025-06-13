from enum import IntEnum

class IndexTypeLabel(IntEnum):
    SEQUENTIAL  = 0
    AVL         = 1
    ISAM        = 2
    HASH        = 3
    BTREE       = 4
    RTREE       = 5