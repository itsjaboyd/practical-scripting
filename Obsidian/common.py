"""common.py: Commonly used functions across Obsidian scripting"""

import pathlib


def read_file_contents(file_path):
    if not isinstance(file_path, pathlib.Path):
        file_path = pathlib.Path(file_path)
    with open(file_path, "r") as fp:
        contents = fp.read()
        return contents


def write_file_contents(file_path, contents):
    if not isinstance(file_path, pathlib.Path):
        file_path = pathlib.Path(file_path)
    with open(file_path, "w") as fp:
        fp.write(contents)
        return True


def gather_files(root_path):
    if not isinstance(root_path, pathlib.Path):
        root_path = pathlib.Path(root_path)
    file_list = []
    for fp in root_path.rglob("*.md"):
        if fp.is_file():
            file_list.append(fp)
    return file_list
