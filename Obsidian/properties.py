import common
import pathlib
import importlib

sap = importlib.import_module("search-and-replace")

PROPERTY_DELIMETER = "---\n"


# TODO:
# 3. instead of handing read_lines everywhere, write a function to get property lines.
# 4. Write some of the more useful functions since those will be used in others.


def has_property(read_lines):
    count = 0
    for line in read_lines:
        count = count + 1 if line == PROPERTY_DELIMETER else count
    return True if count == 2 else False


def file_has_properties(file_path):
    read_lines = common.read_file_lines(file_path)
    return has_property(read_lines)


def get_property_delimeter_indeces(read_lines):
    if not has_property(read_lines):
        return None, None
    first, second = None, None
    for index in range(len(read_lines)):
        if read_lines[index] == PROPERTY_DELIMETER:
            first = index if first is None else first
            second = index if first is not None else second
    return first, second


def has_property_key(read_lines, key, return_index=False):
    if not has_property(read_lines):
        return False
    key = f"{key}:"
    first, second = get_property_delimeter_indeces(read_lines)
    for index in range(len(read_lines)):
        if key in read_lines[index] and index in range(first, second):
            return index if return_index else True
    return False


def get_property_indeces(read_lines, key):
    if not has_property_key(read_lines, key):
        return None, None
    key = f"{key}:"
    property_start, property_end = get_property_delimeter_indeces(read_lines)
    start, end = None, None
    for index in range(property_start, property_end):
        current_line = read_lines[index]
        if start is not None:
            line_parts = current_line.split(" ")
            if ":" in line_parts[0]:
                return start, end
            end = index
        if key in current_line:
            start, end = index, index
    return start, end


def get_property_value(read_lines, key):
    if not has_property_key(read_lines, key):
        return
    values = []
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
    read_lines = common.read_file_lines(file_path)
    start, end = get_property_indeces(read_lines, key)
    if start is None or end is None:
        return False
    del read_lines[start : end + 1]
    return read_lines if not write else common.write_file_lines(file_path, read_lines)


def add_property(file_path, key, value):
    read_lines = common.read_file_lines(file_path)
    if has_property_key(read_lines, key):
        return None
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
    read_lines = common.read_file_lines(file_path)
    index = has_property_key(read_lines, key, return_index=True)
    if not index and isinstance(index, bool):
        add_property(file_path, key, value)
        return True
    read_lines = delete_property(file_path, key, write=False)
    read_lines = handle_lines_insert_value(read_lines, index, key, value)
    return common.write_file_lines(file_path, read_lines)


def extract_property_key_line(read_line):
    separated = read_line.split(":", maxsplit=1)
    if len(separated) < 2:
        return None
    return separated[0].strip()


def alphabetize_property(file_path, replace=True):
    # take the property list and alphabetize it.
    properties = get_property_json(file_path)
    sorted_properties = dict(sorted(properties.items()))
    return write_property_json(file_path, sorted_properties, replace=replace)


def group_property(file_path, alphabetize=True, replace=True):
    # take the property, group it by type, and optionally alphabetize it.
    items = []
    lookup = {"texts": [], "numbers": [], "checks": [], "dates": [], "lists": []}
    properties = get_property_json(file_path)
    for key, value in properties.items():
        if isinstance(value, list):
            lookup["lists"].append((key, value))
        elif value.lower() == "true" or value.lower() == "false":
            lookup["checks"].append((key, value))
        elif value.replace(".", "", 1).isdigit():
            lookup["numbers"].append((key, value))
        elif sap.is_in_contents(value, sap.ISO_DATE_REGEX):
            lookup["dates"].append((key, value))
        else:  # the most typical value in properties are just text
            lookup["texts"].append((key, value))
    for key in lookup:
        items.extend(sorted(lookup[key]) if alphabetize else lookup[key])
    return write_property_json(file_path, dict(items), replace=replace)


def redact_property(file_path):
    properties = get_property_json(file_path)
    for key in properties:
        properties[key] = "REDACTED"
    return write_property_json(file_path, properties)


def print_property(file_path, key):
    # print what is currently in property to the console.
    properties = get_property_json(file_path)
    if key not in properties:
        raise ValueError(f"{key} was not found in properties!")
    print(properties[key])


def get_property_json(file_path, dictionary=True):
    # get the property and return it as a json/dict object.
    read_lines = common.read_file_lines(file_path)
    start, end = get_property_delimeter_indeces(read_lines)
    property_lookup = {}
    if start is None or end is None:
        return property_lookup
    for index in range(start + 1, end):
        key = extract_property_key_line(read_lines[index])
        if not key:
            continue
        value = get_property_value(read_lines, key)
        property_lookup[key] = value
    return property_lookup


def write_property_json(file_path, properties, replace=True):
    property_lines = build_properties_lines(properties, delimeters=replace)
    if replace:
        if delete_properties(file_path):
            return common.file_add_lines(file_path, property_lines, index=0)
        return False
    start, end = get_property_delimeter_indeces(read_lines)
    return common.file_add_lines(file_path, property_lines, index=end)


def build_properties_lines(properties, delimeters=True):
    # given a dictionary of properties, turn it into file lines.
    property_lines = [PROPERTY_DELIMETER] if delimeters else []
    for key in properties:
        match properties[key]:
            case list():
                property_lines.append(f"{key}:\n")
                for item in properties[key]:
                    property_lines.append(f"  - {item}\n")
            case bool():
                value = properties[key]
                line_format = f"{key}: {'true' if value else 'false'}\n"
                property_lines.append(line_format)
            case _:
                line_format = f"{key}: {properties[key]}\n"
                property_lines.append(line_format)
    if delimeters:
        property_lines.append(PROPERTY_DELIMETER)
    return property_lines


def delete_properties(file_path):
    # remove the properties section entirely
    read_lines = common.read_file_lines(file_path)
    start, end = get_property_delimeter_indeces(read_lines)
    read_lines = read_lines[:start] + read_lines[end + 1 :]
    return common.write_file_lines(file_path, read_lines)


def rename_property_key(file_path, key, replacement):
    read_lines = common.read_file_lines(file_path)
    index = has_property_key(read_lines, key, return_index=True)
    key, replacement = f"{key}:", f"{replacement}:"
    if isinstance(index, int):
        replaced = read_lines[index].replace(key, replacement)
        read_lines[index] = replaced
    return common.write_file_lines(file_path, read_lines)


def get_property_keys(file_path):
    properties = get_property_json(file_path)
    return properties.keys()


def get_property_values(file_path):
    properties = get_property_json(file_path)
    return properties.values()
