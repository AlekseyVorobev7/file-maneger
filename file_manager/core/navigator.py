import os
import shutil
from core.security import is_safe_path, resolve_safe


class Navigator:
    def __init__(self, base_dir: str):
        self.base_dir = os.path.realpath(base_dir)
        os.makedirs(self.base_dir, exist_ok=True)
        self.current_dir = self.base_dir

    def pwd(self) -> str:
        rel = os.path.relpath(self.current_dir, self.base_dir)
        return "/" if rel == "." else "/" + rel.replace(os.sep, "/")

    def list_dir(self) -> list[tuple[str, str]]:
        entries = []
        for name in sorted(os.listdir(self.current_dir)):
            full = os.path.join(self.current_dir, name)
            kind = "DIR" if os.path.isdir(full) else "FILE"
            entries.append((name, kind))
        return entries

    def change_dir(self, path: str) -> None:
        if path == "..":
            candidate = os.path.dirname(self.current_dir)
        elif path == "/":
            self.current_dir = self.base_dir
            return
        else:
            candidate = resolve_safe(self.base_dir, self.current_dir, path)
        if not is_safe_path(self.base_dir, candidate):
            raise PermissionError("Cannot navigate outside the working directory.")
        if not os.path.isdir(candidate):
            raise NotADirectoryError(f"'{path}' is not a directory.")
        self.current_dir = candidate

    def make_dir(self, name: str) -> None:
        target = resolve_safe(self.base_dir, self.current_dir, name)
        if os.path.exists(target):
            raise FileExistsError(f"Directory '{name}' already exists.")
        os.makedirs(target)

    def remove_dir(self, name: str) -> None:
        target = resolve_safe(self.base_dir, self.current_dir, name)
        if not os.path.isdir(target):
            raise NotADirectoryError(f"'{name}' is not a directory.")
        shutil.rmtree(target)
