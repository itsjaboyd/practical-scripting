import pathlib
import re
import common
import importlib

properties = importlib.import_module("properties")

DATAVIEW_DELIMETER = "```dataview"
DATAVIEW_QUERY_REGEX = r'`{3}dataview([^`{3}]|\n)*`{3}'
ISO_DATE_REGEX = r'\d{4}-\d{2}-\d{2}'


def is_in_contents(contents, pattern, regex=True):
    if not regex:
        return pattern in contents
    return re.search(pattern, contents) is not None


def is_in_lines(lines, pattern, regex=True):
    for line in lines:
        if not regex and pattern in line:
            return True
        if regex and is_in_content(line, pattern):
            return True
    return False


def is_in_file(file_path, searchable, lines=False, regex=True):
    if not lines:
        contents = common.read_file_contents(file_path)
        return is_in_contents(contents, searchable, regex=regex)
    read_lines = common.read_file_lines(file_path)
    return is_in_lines(read_lines, searchable, regex=regex)


def is_in_files(root_path, searchable, lines=False, regex=True):
    file_list = common.gather_files(root_path)
    results = []
    for file_path in file_list:
        found = is_in_file(file_path, searchable, lines=lines, regex=regex)
        results.append((file_path, found))
    return results


def remove_in_content(contents, pattern, count=0, regex=True):
    if not regex:
        if count > 0:
            return contents.replace(pattern, "", count=count)
        return contents.replace(pattern, "")
    return re.sub(pattern, "", contents, count=count)


def replace_in_content(contents, pattern, replacement, count=0, regex=True):
    if not regex:
        if count > 0:
            return contents.replace(pattern, replacement, count=count)
        return contents.replace(pattern, replacement)
    return re.sub(pattern, replacement, contents, count=count)


def remove_in_lines(lines, pattern, count=0, regex=True, remove=True):
    removal_indeces = []
    for index in range(len(lines)):
        removal = lines[index]
        regex_remove = re.sub(pattern, "", lines[index], count=count)
        string_remove = lines[index].replace(pattern, "", count=count)
        removal = regex_remove if regex else string_remove
        lines[index] = removal
        if removal.strip() == "":
            removal_indeces.append(index)
    return common.remove_list_indeces(lines, removal_indeces) if remove else lines


def replace_in_lines(lines, pattern, replacement, count=0, regex=True, remove=True):
    removal_indeces = []
    for index in range(len(lines)):
        regex_replace = re.sub(pattern, replacement, lines[index], count=count)
        string_replace = lines[index].replace(pattern, replacement, count=count)
        replaced = regex_replace if regex else string_replace
        lines[index] = replaced
        if removal.strip() == "":
            removal_indeces.append(index)
    return common.remove_list_indeces(lines, removal_indeces) if remove else lines


def get_matching_groups(pattern, contents):
    results = re.finditer(pattern, contents)
    return [match.group() for match in results]


def truncate_timed_iso_dates(file_path):
    re_iso_time = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}"
    contents = common.read_file_contents(file_path)

    def handle_timed(match):
        timed_iso = match.group()
        corrected_iso = timed_iso.split(" ")[0]
        return corrected_iso

    contents = replace_in_content(contents, re_iso_time, handle_timed)
    return common.write_file_contents(file_path, contents)


def replace_in_file(
    file_path, pattern, replacement, count=0, regex=True, format_function=None
):
    # replace the pattern with replacement in a file.
    if callable(format_function) and format_function is not None:
        replacement = format_function(file_path, replacement)

    contents = common.read_file_contents(file_path)
    contents = replace_in_content(
        contents, pattern, replacement, count=count, regex=regex
    )
    return common.write_file_contents(file_path, contents)


def replace_in_files(
    root_path, pattern, replacement, count=0, regex=True, format_function=None
):
    # replace the pattern with replacement across multiple files.
    file_list = common.gather_files(root_path)
    results = []
    for file_path in file_list:
        result = replace_in_file(
            file_path,
            pattern,
            replacement,
            count=count,
            regex=regex,
            format_function=format_function,
        )
        results.append((file_path, result))
    return results


def remove_in_file(file_path, pattern, count=0, regex=True):
    # remove the pattern with an empty string in a file.
    contents = common.read_file_contents(file_path)
    contents = remove_in_content(contents, pattern, count=count, regex=regex)
    return common.write_file_contents(file_path, contents)


def remove_in_file_lines(file_path, pattern, count=0, regex=True, remove=True):
    read_lines = common.file_read_lines(file_path)
    read_lines = remove_in_lines(
        lines, pattern, count=count, regex=regex, remove=remove
    )
    return common.write_file_lines(file_path, read_lines)


def remove_in_files(root_path, pattern, count=0, regex=True):
    # remove the pattern with an emptry string across multiple files.
    file_list = common.gather_files(root_path)
    results = []
    for file_path in file_list:
        result = remove_in_file(file_path, pattern, count=count, regex=regex)
        results.append((file_path, result))
    return results


def remove_in_files_lines(root_path, pattern, count=0, regex=True, remove=True):
    file_list = common.gather_files(root_path)
    results = []
    for file_path in file_list:
        result = remove_in_file_lines(
            file_path, pattern, count=count, regex=regex, remove=remove
        )
        results.append((file_path, result))
    return results


def file_remove_consecutive_duplicate_lines(file_path, removal="\n", limit=1):
    read_lines = common.read_file_lines(file_path)
    read_lines = remove_consecutive_duplicate_lines(
        read_lines, removal=removal, limit=limit
    )
    return common.write_file_lines(file_path, read_lines)


def remove_consecutive_duplicate_lines(read_lines, removal="\n", limit=1):
    counter, remove_indeces = 0, []
    for index in range(len(read_lines)):
        counter = counter + 1 if read_lines[index] == removal else 0
        if counter > limit:
            remove_indeces.append(index)
    return common.remove_list_indeces(read_lines, remove_indeces)


def delete_newlines_before_queries(read_lines, empty="\n"):
    remove_indeces = []
    for index in range(len(read_lines)):
        if DATAVIEW_DELIMETER in read_lines[index] and index != 0:
            counter, newlines = index, True
            while newlines:
                counter -= 1
                if read_lines[counter] == empty:
                    remove_indeces.append(counter)
                else:
                    newlines = False
    return common.remove_list_indeces(read_lines, remove_indeces)


def file_delete_newlines_before_queries(file_path, empty="\n"):
    read_lines = common.read_file_lines(file_path)
    read_lines = delete_newlines_before_queries(read_lines, empty=empty)
    return common.write_file_lines(file_path, read_lines)


def files_delete_newlines_before_queries(root_path, empty="\n"):
    file_list = common.gather_files(root_path)
    results = []
    for file_path in file_list:
        result = file_delete_newlines_before_queries(file_path, empty=empty)
        results.append((file_path, result))
    return results


def search_in_file(file_path, pattern, count=0, regex=True):
    # return matches based on the pattern in the file.
    pass


def search_in_files(root_path, pattern, count=0, regex=True):
    # return matches across files based on the pattern.
    pass


# Useful and common format functions


def format_on_property_values(file_path, initial_string):
    # note that initial string must have formats named as {values[key]} where
    # key is the property value's key to replace with.
    props = properties.get_property_json(file_path)
    try:
        result = initial_string.format(props=props)
        return result
    except KeyError as ke:
        print(f"Cannot format without properties: {ke}")
        return initial_string
    except:
        return initial_string
