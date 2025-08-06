import pathlib
import re
import common
import platform


if platform.system() == "Darwin":
    BASE_PATH = "/Users/jasonboyd/Tracking/"
else:  # use WSL's path to user notes on windows WSL
    BASE_PATH = "/mnt/c/Users/basonjoyd/Tracking/"


def repair_old_meeting(contents):
    query_regex = (
        r"`{3}dataview\nTABLE summary, created\nFROM \"Meetings\"\nWHERE "
        r"any\(map\(attendees, \(a\) \=> a \= this.title\)\)\n`{3}"
    )
    replacement = (
        r"```dataview\n"
        r'TABLE summary as "Summary", transpired as "Transpired"\n'
        r'FROM "Meetings"\n'
        r"WHERE any(map(attendees, (a) => a = this.link))\n"
        r"SORT created DESC\n"
        r"```"
    )
    match_list = find_match_strings(query_regex, contents)
    if not match_list:
        return False
    return re.sub(query_regex, replacement, contents)


def find_match_strings(pattern, contents):
    results = re.finditer(pattern, contents)
    return [match.group() for match in results]


def repair_timed_iso_dates(contents):
    re_iso_time = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}"
    match_list = find_match_strings(re_iso_time, contents)
    if not match_list:
        return contents
    for match in match_list:
        corrected_iso = match.split(" ")[0]
        contents = contents.replace(match, corrected_iso, 1)
    return contents


def repair_file_timed_iso_dates(file_path):
    contents = common.read_file_contents(file_path)
    contents = repair_timed_iso_dates(contents)
    return common.write_file_contents(file_path, contents)


def repair_files_timed_iso_dates(root_path):
    file_list = common.gather_files(root_path)
    results = []
    for file_path in file_list:
        result = repair_file_timed_iso_dates(file_path)
        status = "success" if result else "failure"
        message = f"Updating timed iso dates resulted {status} for {file_path}."
        results.append(message)
    return results


def repair_files_with_function(root_path, regex_function):
    file_list = common.gather_files(root_path)
    results = [
        repair_file_with_function(fp, regex_function) for fp in file_list
    ]
    return results


def repair_file_with_function(file_path, regex_function):
    if not callable(regex_function):
        raise ValueError("Supplied function is uncallable!")
    contents = common.read_file_contents(file_path)
    contents = regex_function(contents)
    return common.write_file_contents(file_path, contents)


def main():
    sarah = BASE_PATH + "People/sarah-gregory.md"
    result = repair_file_with_function(sarah, repair_old_meeting)
    print(result)


if __name__ == "__main__":
    main()
