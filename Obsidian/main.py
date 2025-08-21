import importlib
import datetime
import platform

common = importlib.import_module("common")
properties = importlib.import_module("properties")
sap = importlib.import_module("search-and-replace")
upc = importlib.import_module("update-people-contacted")


if platform.system() == "Darwin":
    BASE_PATH = "/Users/jasonboyd/Tracking/"
else:  # use WSL's path to user notes on windows WSL
    BASE_PATH = "/mnt/c/Users/basonjoyd/Tracking/"

bad_hobbies = r'```dataview\s*\n\s*TABLE summary as "Summary", attendees as "Attendees"\s*\n\s*FROM "Meetings"\s*\n\s*WHERE file.cday = date\(".{0,20}"\)\n```'
hobbies_replace = """```dataview
TABLE title as "Title", type as "Type"
FROM #hobby AND !"Extras"
WHERE date(transpired) = date(this.created)
```"""

def main():
    root_path = BASE_PATH + "Periodicals/Dailys/2024/August/"
    files = common.gather_files(root_path)
    for file_path in files:
        result = sap.replace_in_file(file_path, bad_hobbies, hobbies_replace)
        print(file_path, result)


if __name__ == "__main__":
    main()
