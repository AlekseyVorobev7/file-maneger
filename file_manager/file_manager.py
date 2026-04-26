import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from core.navigator import Navigator
from core.file_ops import FileOperations
from ui.cli import run

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")


def load_config() -> dict:
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_working_dir(config: dict) -> str:
    wd = config.get("working_directory", "./workspace")
    if not os.path.isabs(wd):
        wd = os.path.join(os.path.dirname(CONFIG_FILE), wd)
    return os.path.realpath(wd)


def main() -> None:
    config = load_config()
    base_dir = resolve_working_dir(config)

    navigator = Navigator(base_dir)
    file_ops = FileOperations(navigator)

    run(navigator, file_ops)


if __name__ == "__main__":
    main()
