import common
import pathlib

PROPERTY_DELIMETER = "---\n"


def get_read_lines(contents):
    if isinstance(contents, list):
        return contents
    return common.read_file_lines(contents)


def has_property(contents):
    read_lines = get_read_lines(contents)
    if read_lines.count(PROPERTY_DELIMETER) == 2:
        return True
    return False


def get_property_delimeter_indeces(contents):
    if not has_property(contents):
        return None, None
    read_lines = get_read_lines(contents)
    first, second = None, None
    for index in range(len(read_lines)):
        if read_lines[index] == PROPERTY_DELIMETER:
            first = index if first is None else first
            second = index if first is not None else second
    return first, second


def has_property_key(contents, key, return_index=False):
    if not has_property(contents):
        return False
    key = f"{key}:"
    read_lines = get_read_lines(contents)
    first, second = get_property_delimeter_indeces(read_lines)
    for index in range(len(read_lines)):
        if key in read_lines[index] and index in range(first, second):
            return index if return_index else True
    return False


def get_property_indeces(contents, key):
    if not has_property_key(contents, key):
        return None, None
    key = f"{key}:"
    fm_start, fm_end = get_property_delimeter_indeces(contents)
    read_lines = get_read_lines(contents)
    start, end = None, None
    for index in range(fm_start, fm_end):
        current_line = read_lines[index]
        if start is not None:
            line_parts = current_line.split(" ")
            if ":" in line_parts[0]:
                return start, end
            end = index
        if key in current_line:
            start, end = index, index
    return start, end


def get_property_value(contents, key):
    if not has_property_key(contents, key):
        return
    values = []
    read_lines = get_read_lines(contents)
    start, end = get_property_indeces(read_lines, key)
    for index in range(start, end + 1):
        line_parts = read_lines[index].split(" ")
        assembled_value = " ".join(line_parts[1:])
        stripped_value = assembled_value.strip()
        values.append(stripped_value)
    if len(values) == 1:
        return values[-1]
    return clean_property_values(values)


def clean_property_values(values):
    cleaned_values = []
    for value in values:
        if value:
            clean_value = value.replace("- ", "")
            cleaned_values.append(clean_value)
    return cleaned_values


def delete_property(file_path, key, write=True):
    read_lines = get_read_lines(file_path)
    start, end = get_property_indeces(read_lines, key)
    if start is None or end is None:
        return False
    del read_lines[start : end + 1]
    return read_lines if not write else common.write_file_lines(file_path, read_lines)


def add_property(file_path, key, value):
    read_lines = get_read_lines(file_path)
    start, end = get_property_delimeter_indeces(read_lines)
    if start is None or end is None:
        return False
    read_lines = handle_lines_insert_value(read_lines, end, key, value)
    return common.write_file_lines(file_path, read_lines)


def insert_list_at_index(supplied_list, index, insert_list):
    if index not in range(len(supplied_list)):
        raise ValueError("Supplied index out of range!")
    if not isinstance(supplied_list, list):
        raise ValueError("Supplied list is not list type!")
    for insert_item in insert_list:
        supplied_list.insert(index, insert_item)
        index += 1
    return supplied_list


def handle_lines_insert_value(read_lines, index, key, value):
    if not isinstance(read_lines, list):
        raise ValueError("Supplied list is not list type!")
    if isinstance(value, list):
        value = [f"  - {v}\n" for v in value]
        insert_list = [f"{key}:\n", *value]
        read_lines = insert_list_at_index(read_lines, index, insert_list)
    else:
        addition = f"{key}: {value}\n"
        read_lines.insert(index, addition)
    return read_lines


def update_property(file_path, key, value):
    read_lines = get_read_lines(file_path)
    index = has_property_key(read_lines, key, return_index=True)
    if not index and isinstance(index, bool):
        add_property(file_path, key, value)
        return True
    read_lines = delete_property(read_lines, key, write=False)
    read_lines = handle_lines_insert_value(read_lines, index, key, value)
    return common.write_file_lines(file_path, read_lines)


def alphatbetize_property(file_path):
    # take the property list and alphabetize it.
    pass


def group_property(file_path, alphabetize=True):
    # take the property, group it by type, and optionally alphabetize it.
    pass


def redact_property(file_path):
    # replace property values with some redacted nullified field.
    pass


def remove_property(file_path):
    # remove the property portion entirely.
    pass


def replace_property(file_path, keys, values):
    # replace property key(s) with new value(s).
    pass


def print_property(file_path):
    # print what is currently in property to the console.
    pass


def get_property_json(file_path, dictionary=True):
    # get the property and return it as a json/dict object.
    pass


def get_property_keys(file_path):
    # return the property keys as a list.
    pass


def get_property_values(file_path):
    # return the property values as a list.
    pass


def guess_property_type(file_path, key):
    # guess the property key type based on its value.
    pass


def file_has_frontmatter(file_path):
    # return boolean based on if property exists or not.
    pass
