from abc import ABC
from pathlib import Path

from server.storage.disk.path_builder import PathBuilder
from server.storage.disk.file_manager import FileManager

class BaseService(ABC):
    def __init__(self, file_manager: FileManager, path_builder: PathBuilder):
        self.file_manager = file_manager
        self.path_builder = path_builder

    def _ensure_directory_exists(self, path: Path) -> None:
        if not self.file_manager.path_exists(path):
            self.file_manager.create_directory(path)
    
    def _ensure_file_exists(self, path: Path) -> None:
        if not self.file_manager.path_exists(path):
            self.file_manager.create_file(path)