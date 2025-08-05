"""common.py: Commonly used functions across Obsidian scripting"""

import pathlib


def get_path(file_path):
    if not isinstance(file_path, pathlib.Path):
        file_path = pathlib.Path(file_path)
    return file_path


def read_file_contents(file_path):
    file_path = get_path(file_path)
    with open(file_path, "r") as fp:
        contents = fp.read()
        return contents


def read_file_lines(file_path):
    file_path = get_path(file_path)
    with open(file_path, "r") as fp:
        lines = fp.readlines()
        return lines


def write_file_lines(file_path, write_lines):
    file_path = get_path(file_path)
    with open(file_path, "w") as fp:
        fp.writelines(write_lines)
        return True


def write_file_contents(file_path, contents):
    file_path = get_path(file_path)
    with open(file_path, "w") as fp:
        fp.write(contents)
        return True


def gather_files(root_path):
    root_path = get_path(root_path)
    file_list = []
    for fp in root_path.rglob("*.md"):
        if fp.is_file():
            file_list.append(fp)
    return file_list
