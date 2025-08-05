import common
import pathlib

FRONT_MATTER_DELIMETER = "---\n"


def get_read_lines(contents):
    if isinstance(contents, list):
        return contents
    return common.read_file_lines(contents)


def has_front_matter(contents):
    read_lines = get_read_lines(contents)
    if read_lines.count(FRONT_MATTER_DELIMETER) == 2:
        return True
    return False


def get_front_matter_delimeter_indeces(contents):
    if not has_front_matter(contents):
        return None, None
    read_lines = get_read_lines(contents)
    first, second = None, None
    for index in range(len(read_lines)):
        if read_lines[index] == FRONT_MATTER_DELIMETER:
            first = index if first is None else first
            second = index if first is not None else second
    return first, second


def has_front_matter_key(contents, key):
    if not has_front_matter(contents):
        return False
    key = f"{key}:"
    read_lines = get_read_lines(contents)
    first, second = get_front_matter_delimeter_indeces(read_lines)
    for index in range(len(read_lines)):
        if key in read_lines[index] and index in range(first, second):
            return True
    return False


def get_front_matter_indeces(contents, key):
    if not has_front_matter_key(contents, key):
        return None, None
    key = f"{key}:"
    fm_start, fm_end = get_front_matter_delimeter_indeces(contents)
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


def get_front_matter_value(contents, key):
    if not has_front_matter_key(contents, key):
        return
    values = []
    read_lines = get_read_lines(contents)
    start, end = get_front_matter_indeces(read_lines, key)
    for index in range(start, end + 1):
        line_parts = read_lines[index].split(" ")
        assembled_value = " ".join(line_parts[1:])
        stripped_value = assembled_value.strip()
        values.append(stripped_value)
    if len(values) == 1:
        return values[-1]
    return clean_front_matter_values(values)


def clean_front_matter_values(values):
    cleaned_values = []
    for value in values:
        if value:
            clean_value = value.replace("- ", "")
            cleaned_values.append(clean_value)
    return cleaned_values


def delete_front_matter(file_path, key):
    read_lines = get_read_lines(file_path)
    start, end = get_front_matter_indeces(read_lines, key)
    if start is None or end is None:
        return False
    del read_lines[start : end + 1]
    return common.write_file_lines(file_path, read_lines)


def add_front_matter(contents, key, value):
    pass


def udpate_front_matter(contents, key, value):
    pass


def testing():
    # myf = "/Users/jasonboyd/Tracking/Meetings/2025/August/jordanelle-sunday-sailing-dinner.md"
    myf = "/Users/jasonboyd/Tracking/testing-front-matter.md"
    for el in get_read_lines(myf):
        print(repr(el))
    print()
    indeces = get_front_matter_indeces(myf, "tags")
    print(indeces)
    values = get_front_matter_value(myf, "tags")
    print(values)


def main():
    myf = "/Users/jasonboyd/Tracking/testing-front-matter.md"
    result = delete_front_matter(myf, "summary")
    print(result)


if __name__ == "__main__":
    main()
