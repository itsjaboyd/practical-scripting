import importlib
import re

sap = importlib.import_module("search-and-replace")
fm = importlib.import_module("front-matter")
common = importlib.import_module("common")

MEETINGS_SECTION_BAD = """
## Meetings

```dataview
TABLE summary as "Summary", created as "Created"
FROM "Meetings"
WHERE any(map(attendees, (a) => a = this.title))
```

"""

MEETINGS_SECTION_APPEND = """

## Meetings
```dataview
TABLE summary as "Summary", transpired as "Transpired"
FROM "Meetings"
WHERE any(map(attendees, (a) => a = this.link))
SORT created DESC
```"""


def remove_pattern(file_path, pattern, regex=True):
    contents = common.read_file_contents(file_path)
    replaced = sap.remove_in_content(contents, pattern, regex=regex)
    return common.write_file_contents(file_path, replaced)


def replace_pattern(file_path, pattern, replacement, count=0, regex=True):
    contents = common.read_file_contents(file_path)
    replaced = sap.replace_in_content(
        contents, pattern, replacement, count=count, regex=regex
    )
    return common.write_file_contents(file_path, replaced)


def remove_pattern_append_addition(file_path, pattern, addition, count=0, regex=True):
    contents = common.read_file_contents(file_path)
    contents = common.strip_contents(contents)
    contents = sap.remove_in_content(contents, pattern, count=count, regex=regex)
    contents = common.add_content(contents, addition)
    return common.write_file_contents(file_path, contents)


def files_apply_function(root_path, apply_function, args, kwargs):
    apply_results = []
    for file_path in common.gather_files(root_path):
        result = apply_function(file_path, *args, **kwargs)
        apply_results.append((file_path, result))
    return apply_results


def main():
    #sarah = BASE_PATH + "People/sarah-gregory.md"
    #result = remove_pattern_append_addition(
    #    sarah, MEETINGS_SECTION_BAD, MEETINGS_SECTION_APPEND, regex=False
    #)
    #print(result)

    root_path = BASE_PATH + "People/Testing/"
    args = [MEETINGS_SECTION_BAD, MEETINGS_SECTION_APPEND]
    kwargs = {"regex": False}
    results = files_apply_function(
        root_path, remove_pattern_append_addition, args, kwargs
    )
    for el in results:
        print(el)


if __name__ == "__main__":
    main()
