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


def main():
    note_path = BASE_PATH + "Testing/2025-07-08.md"
    result = properties.delete_properties(note_path)
    print(result)

if __name__ == "__main__":
    main()
