from enum import IntEnum

class DataTypeLabel(IntEnum):
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
    JSONB       = 12
    DECIMAL     = 13

# Categorías de tipos de datos
class IntegerTypeSize(IntEnum):
    SMALLINT    = 2
    INT         = 4
    BIGINT      = 8
    
class NumericTypeSize(IntEnum):
    DOUBLE      = 8
    DECIMAL     = -1

class TemporalTypeSize(IntEnum):
    DATE        = 4
    TIME        = 8
    TIMESTAMP   = 8

class OtherTypeSize(IntEnum):
    BOOLEAN     = 1
    UUID        = 16
    GEOMETRIC   = -1
    JSONB       = -1