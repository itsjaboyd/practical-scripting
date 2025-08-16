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


LEARNING_TABLE = r'## Learning\n\n.*\n\n```dataview\nTABLE title as "Title", summary as "Summary"\nFROM "Subjects" OR "Courses"\nWHERE contains\(flat\(list\(updated\)\), date\(".{0,20}"\)\)\n```'

WORKOUT_TABLE = r'```dataview\nTABLE type as "Workout Type", mood as "Overall Mood", effort as "Overall Effort" \nFROM "Fitness"\nWHERE date\(split\(transpired, " "\)\[0\]\) = date\(".{0,20}"\)\n```'

REPLACEMENT = r'```dataview\nTABLE title as "Title", type as "Type"\nFROM #health OR #fitness AND !"Extras"\nWHERE date(transpired) = date("{values[created]}")\nOR date(created) = date("{values[created]}")\n```'


def main():
    target_daily = BASE_PATH + "Periodicals/Dailys/2025/July/2025-07-29.md"
    print(sap.is_in_file(target_daily, WORKOUT_TABLE))
    result = sap.replace_in_file(
        target_daily,
        WORKOUT_TABLE,
        REPLACEMENT,
        format_function=sap.format_on_property_values,
    )
    print(result)


if __name__ == "__main__":
    main()
