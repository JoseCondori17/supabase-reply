from dataclasses import dataclass
from pathlib import Path

@dataclass
class Index:
    idx_id          : int
    idx_type        : int
    idx_name        : str
    idx_file        : Path
    idx_tuples      : int
    idx_columns     : list[int]  # column positions
    idx_is_primary  : bool