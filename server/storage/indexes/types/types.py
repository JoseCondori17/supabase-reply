from enum import IntEnum

class IndexType(IntEnum):
    SEQUENTIAL  = 0
    AVL         = 1
    ISAM        = 2
    HASH        = 3
    BTREE       = 4
    RTREE       = 5

class DataType(IntEnum):
    SMALLINT    = 0
    INT         = 1
    BIGINT      = 2
    DOUBLE      = 3
    CHAR        = 4
    VARCHAR     = 5
    BOOLEAN     = 6
    UUID        = 7
    DATE        = 8
    TIME        = 9
    TIMESTAMP   = 10
    GEOMETRIC   = 11
    JSON        = 12
    DECIMAL     = 13