import os


def is_safe_path(base_dir: str, path: str) -> bool:
    base = os.path.realpath(base_dir)
    target = os.path.realpath(path)
    return target == base or target.startswith(base + os.sep)


def resolve_safe(base_dir: str, current_dir: str, rel_path: str) -> str:
    candidate = os.path.join(current_dir, rel_path)
    if not is_safe_path(base_dir, candidate):
        raise PermissionError(f"Access denied: cannot leave working directory '{base_dir}'")
    return os.path.realpath(candidate)
