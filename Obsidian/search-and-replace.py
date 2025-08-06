import pathlib
import re
import common

ROOT_DIRECTORY = "/Users/jasonboyd/Tracking/"


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


def main():
    pattern = r''
    sarah = ROOT_DIRECTORY + "People/sarah-gregory.md"
    contents = common.read_file_contents(sarah)
    print(contents)


if __name__ == "__main__":
    main()
