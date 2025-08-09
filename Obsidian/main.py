import importlib
import platform

common = importlib.import_module("common")
fm = importlib.import_module("front-matter")
sap = importlib.import_module("search-and-replace")
mn = importlib.import_module("modify-notes")
upc = importlib.import_module("update-people-contacted")


if platform.system() == "Darwin":
    BASE_PATH = "/Users/jasonboyd/Tracking/"
else:  # use WSL's path to user notes on windows WSL
    BASE_PATH = "/mnt/c/Users/basonjoyd/Tracking/"

def main():
    upc.generate_updated_meetings_json()


if __name__ == "__main__":
    main()
