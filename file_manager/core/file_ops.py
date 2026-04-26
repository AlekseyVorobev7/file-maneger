import os
import shutil
from core.security import resolve_safe


class FileOperations:
    def __init__(self, navigator):
        self.nav = navigator

    def _resolve(self, name: str) -> str:
        return resolve_safe(self.nav.base_dir, self.nav.current_dir, name)

    def create_file(self, name: str) -> None:
        target = self._resolve(name)
        if os.path.exists(target):
            raise FileExistsError(f"File '{name}' already exists.")
        open(target, "w", encoding="utf-8").close()

    def read_file(self, name: str) -> str:
        target = self._resolve(name)
        if not os.path.isfile(target):
            raise FileNotFoundError(f"File '{name}' not found.")
        with open(target, "r", encoding="utf-8") as f:
            return f.read()

    def write_file(self, name: str, content: str) -> None:
        target = self._resolve(name)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)

    def append_file(self, name: str, content: str) -> None:
        target = self._resolve(name)
        if not os.path.isfile(target):
            raise FileNotFoundError(f"File '{name}' not found.")
        with open(target, "a", encoding="utf-8") as f:
            f.write(content)

    def delete_file(self, name: str) -> None:
        target = self._resolve(name)
        if not os.path.isfile(target):
            raise FileNotFoundError(f"File '{name}' not found.")
        os.remove(target)

    def copy_file(self, src: str, dst: str) -> None:
        src_path = self._resolve(src)
        dst_path = self._resolve(dst)
        if not os.path.isfile(src_path):
            raise FileNotFoundError(f"Source file '{src}' not found.")
        shutil.copy2(src_path, dst_path)

    def move_file(self, src: str, dst: str) -> None:
        src_path = self._resolve(src)
        dst_path = self._resolve(dst)
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"'{src}' not found.")
        shutil.move(src_path, dst_path)

    def rename_file(self, old_name: str, new_name: str) -> None:
        old_path = self._resolve(old_name)
        new_path = self._resolve(new_name)
        if not os.path.exists(old_path):
            raise FileNotFoundError(f"'{old_name}' not found.")
        if os.path.exists(new_path):
            raise FileExistsError(f"'{new_name}' already exists.")
        os.rename(old_path, new_path)
