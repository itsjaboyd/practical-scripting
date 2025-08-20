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
    translation = str.maketrans({'"': "", "[": "", "]": "", ".": "", "/": ""})
    if isinstance(person_link, list):
        for index in range(len(person_link)):
            initial_strip = person_link[index].translate(translation)
            gathered_name = initial_strip.split("|")[-1]
            person_link[index] = gathered_name
        return person_link
    person_link = person_link.translate(translation)
    return person_link


def strip_lines_handler(supplied_lines, rear=True):
    whitespace = True
    index = 0 if not rear else len(supplied_lines) - 1
    while whitespace:
        lstrip = supplied_lines[index].lstrip()
        rstrip = supplied_lines[index].rstrip()
        initial_strip = lstrip if not rear else rstrip
        supplied_lines[index] = initial_strip
        if initial_strip:
            whitespace = False
        index += 1 if not rear else -1
    return supplied_lines


def strip_lines(supplied_lines):
    for border in [True, False]:
        supplied_lines = strip_lines_handler(supplied_lines, rear=border)
    return remove_empty_lines(supplied_lines)


def remove_empty_lines(supplied_lines):
    real_lines = []
    for line in supplied_lines:
        if line:
            real_lines.append(line)
    return real_lines


def strip_contents(supplied_content):
    return supplied_content.strip()


def add_lines(supplied_lines, lines_list, index=-1):
    if index == -1:
        supplied_lines.extend(lines_list)
    else:
        if index not in range(len(supplied_lines)):
            raise ValueError("Supplied index not within lines!")
        supplied_lines[index:index] = lines_list
    return supplied_lines


def add_content(supplied_content, addition, index=-1):
    if index == -1:
        supplied_content += addition
    else:
        if index not in range(len(contents)):
            raise ValueError("Supplied index not within content!")
        supplied_content = contents[:index] + addition + contents[index:]
    return supplied_content


def file_add_lines(file_path, lines_list, index=-1):
    read_lines = read_file_lines(file_path)
    read_lines = add_lines(read_lines, lines_list, index=index)
    return file_write_lines(file_path, read_lines)


def file_strip_whitespace(file_path):
    contents = read_file_contents(file_path)
    contents = strip_contents(contents)
    return write_file_contents(file_path, contents)


def file_add_content(file_path, addition, index=-1):
    contents = read_file_contents(file_path)
    contents = add_content(contents, addition, index=index)
    return write_file_contents(file_path, contents)


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
