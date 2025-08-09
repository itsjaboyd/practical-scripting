import importlib
import re
import platform

sap = importlib.import_module("search-and-replace")
fm = importlib.import_module("front-matter")
common = importlib.import_module("common")

if platform.system() == "Darwin":
    BASE_PATH = "/Users/jasonboyd/Tracking/"
else:  # use WSL's path to user notes on windows WSL
    BASE_PATH = "/mnt/c/Users/basonjoyd/Tracking/"

BAD_MEETING_STRING = """

## Meetings

```dataview
TABLE summary, created
FROM "Meetings"
WHERE any(map(attendees, (a) => a = this.title))
```
"""


def replace_pattern(file_path, pattern, replacement):
    contents = common.read_file_contents(file_path)
    replaced = sap.replace_in_content(contents, pattern, replacement)
    return common.write_file_contents(file_path, replaced)


def remove_and_append(file_path, pattern, addition, regex=True):
    contents = common.read_file_contents(file_path)
    contents = common.strip_contents(contents)
    contents = sap.remove_in_content(contents, pattern, regex=regex)
    contents = common.add_content(contents, addition)
    return common.write_file_contents(file_path, contents)


def remove_pattern(file_path, pattern, regex=True):
    contents = common.read_file_contents(file_path)
    replaced = sap.remove_in_content(contents, pattern, regex=regex)
    return common.write_file_contents(file_path, replaced)


def main():
    query_regex = (
        r"\n\n## Meetings\n\n"
        r"`{3}dataview\nTABLE summary, created\nFROM \"Meetings\"\nWHERE "
        r"any\(map\(attendees, \(a\) \=> a \= this.title\)\)\n`{3}\n"
    )
    replacement = (
        "\n\n## Meetings\n"
        "```dataview\n"
        'TABLE summary as "Summary", transpired as "Transpired"\n'
        'FROM "Meetings"\n'
        "WHERE any(map(attendees, (a) => a = this.link))\n"
        "SORT created DESC\n"
        "```"
    )
    sarah = BASE_PATH + "People/sarah-gregory.md"
    result = remove_pattern(sarah, BAD_MEETING_STRING, regex=False)
    print(result)


if __name__ == "__main__":
    main()
