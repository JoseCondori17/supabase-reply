import os
import pickle
from pathlib import Path
from dataclasses import dataclass

@dataclass
class FileManager:
    base_path: Path

    def create_file(self, path: Path) -> None:
        with open(path, 'w') as f: pass

    def create_dir(self, path: Path) -> None:
        os.makedirs(path, exist_ok=True)

    def delete_file(self, path: Path) -> None:
        os.remove(path)

    def delete_dir(self, path: Path) -> None:
        os.rmdir(path)

    def path_exists(self, path: Path) -> bool:
        full_path = self.base_path / path
        return full_path.exists()

    def open_file(self, path: Path, read_only: bool):
        mode = 'rb' if read_only else 'w+b'
        return open(path, mode)

    def read_data(self, path: Path) -> any:
        with self.open_file(path, True) as file:
            return pickle.load(file)

    def write_data(self, data: any, path: Path) -> None:
        with self.open_file(path, False) as file:
            pickle.dump(data, file)