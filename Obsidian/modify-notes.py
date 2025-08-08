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


def replace_dataview_query(file_path, pattern, replacement):
    contents = common.read_file_contents(file_path)
    replaced = sap.replace_in_content(contents, pattern, replacement)
    return common.write_file_contents(file_path, replaced)

def delete_dataview_query(file_path, pattern):
    contents = common.read_file_contents(file_path)
    replaced = sap.remove_in_content(contents, pattern)
    return common.write_file_contents(file_path, replaced)

def delete_and_append(flie_path, pattern, addition, regex=True):
    pass
    


def main():
    query_regex = (
        r'`{3}dataview\nTABLE summary, created\nFROM \"Meetings\"\nWHERE '
        r'any\(map\(attendees, \(a\) \=> a \= this.title\)\)\n`{3}'
    )
    replacement = (
        r'```dataview\n'
        r'TABLE summary as "Summary", transpired as "Transpired"\n'
        r'FROM "Meetings"\n'
        r'WHERE any(map(attendees, (a) => a = this.link))\n'
        r'SORT created DESC\n'
        r'```'
    )
    sarah = BASE_PATH + "People/sarah-gregory.md"
    print(sap.is_in_file(sarah, query_regex))



if __name__ == "__main__":
    main()
