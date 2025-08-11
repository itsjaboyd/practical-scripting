import importlib
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
    sarah = BASE_PATH + "People/sarah-gregory.md"
    result = properties.get_property_json(sarah)
    for key in result:
        print(key, result[key])


if __name__ == "__main__":
    main()
