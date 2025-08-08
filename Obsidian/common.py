"""common.py: Commonly used functions across Obsidian scripting"""

import pathlib
import json


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


def sanitize_person_links(person_link):
    translation = str.maketrans({'"': "", "[": "", "]": ""})
    if isinstance(person_link, list):
        for index in range(len(person_link)):
            person_link[index] = person_link[index].translate(translation)
        return person_link
    person_link = person_link.translate(translation)
    return person_link


def file_add_lines(file_path, lines_list, index=-1):
    read_lines = read_file_lines(file_path)
    if index == -1:
        read_lines.extend(lines_list)
    else:
        if index not in range(len(read_lines)):
            return False
        read_lines[index:index] = lines_list
    return write_file_lines(file_path, read_lines)


def file_add_content(file_path, addition, index=-1):
    contents = read_file_contents(file_path)
    if index == -1:
        contents += addition
    else:
        if index not in range(len(contents)):
            return False
        contents = contents[:index] + addition + contents[index:]
    return write_file_contents(file_path)


def remove_list_indeces(supplied_list, index_list):
    if not index_list:
        return supplied_list
    removed_list = []
    for index in range(len(supplied_list)):
        if index not in index_list:
            removed_list.append(supplied_list[index])
    return removed_list


def get_updated_json(file_path):
    file_path = get_path(file_path)
    with open(file_path, "r") as fp:
        return json.load(fp)


def write_updated_json(file_path, updated_json):
    file_path = get_path(file_path)
    with open(file_path, "w") as fp:
        return json.dump(updated_json, fp)
