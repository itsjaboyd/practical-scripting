import pathlib
import re
import common


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


def remove_in_lines(lines, pattern, count=0, regex=True, remove_line=True):
    removal_indeces = []
    for index in range(len(lines)):
        removal = lines[index]
        regex_remove = re.sub(pattern, "", lines[index], count=count)
        string_remove = lines[index].replace(pattern, "", count=count)
        removal = regex_remove if regex else string_remove
        lines[index] = removal
        if removal.strip() == "":
            removal_indeces.append(index)
    return (
        common.remove_list_indeces(lines, removal_indeces)
        if remove_line
        else lines
    )


def replace_in_lines(
    lines, pattern, replacement, count=0, regex=True, remove_line=True
):
    removal_indeces = []
    for index in range(len(lines)):
        regex_replace = re.sub(pattern, replacement, lines[index], count=count)
        string_replace = lines[index].replace(pattern, replacement, count=count)
        replaced = regex_replace if regex else string_replace
        lines[index] = replaced
        if removal.strip() == "":
            removal_indeces.append(index)
    return (
        common.remove_list_indeces(lines, removal_indeces)
        if remove_line
        else lines
    )


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


def main():
    sarah = BASE_PATH + "People/sarah-gregory.md"
    result = apply_sap_function(sarah, repair_old_meeting)
    print(result)


if __name__ == "__main__":
    main()
