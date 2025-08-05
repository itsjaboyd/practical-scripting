import pathlib
import common

ROOT_DIRECTORY = "/Users/jasonboyd/Tracking/People/"


def contents_has_frontmatter(contents):
    if not isinstance(contents, str):
        contents = str(contents)
    results = contents.find("---")
    return False if results == -1 else True


def replace_frontmatter(contents, expected, replace):
    if not isinstance(contents, str):
        contents = str(contents)
    if not contents_has_frontmatter(contents):
        raise ValueError("Frontmatter not found!")
    replaced = contents.replace(expected, replace, 1)
    return replaced


def replace_file_frontmatter(file_path, expected, replace):
    contents = common.read_file_contents(file_path)
    replaced = replace_frontmatter(contents, expected, replace)
    return common.write_file_contents(file_path, replaced)


def replace_files_frontmatter(file_list, expected, replace):
    if not isinstance(file_list, list):
        raise ValueError("File list must be a list!")
    results = []
    for file_path in file_list:
        if not isinstance(file_path, pathlib.Path):
            file_path = pathlib.Path(file_path)
        result = replace_file_frontmatter(file_path, expected, replace)
        status = "success" if result else "failure"
        message = (
            f"Replace {expected} with {replace} resulted {status} for {file_path}."
        )
        results.append(message)
    return results


def fix_people():
    people = common.gather_files(ROOT_DIRECTORY)
    expected, replace = "title", "link"
    results = replace_files_frontmatter(people, expected, replace)
    for result in results:
        print(result)


def main():
    fix_people()


if __name__ == "__main__":
    main()
