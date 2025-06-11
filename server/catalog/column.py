from dataclasses import dataclass

@dataclass
class Column:
    att_name        : str
    att_type_id     : int
    att_len         : int
    att_not_null    : bool
    att_has_def     : bool