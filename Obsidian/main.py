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


LEARNING_TABLE = r'## Learning\n\nPut something you learned today here\.\n\n```dataview\n\s*TABLE title as "Title", summary as "Summary"\n\s*FROM "Subjects" OR "Courses"\n\s*WHERE contains\(flat\(list\(updated\)\), date\(".{0,20}"\)\)\n```'

READING_TABLE = r'## Reading\n\n```dataview\n\s*TABLE title as "Publication", author as "Author", finished as "Finished"\n\s*FROM "Reading"\n\s*WHERE contains\(flat\(list\(\s*updated\s*\)\), date\(".{0,20}"\)\)\n```'

WORKOUT_TABLE = r'```dataview\nTABLE type as "Workout Type", mood as "Overall Mood", effort as "Overall Effort"\s*\nFROM "Fitness"\nWHERE date\(split\(transpired, " "\)\[0\]\) = date\(".{0,20}"\)\n```'

MEETINGS_TABLE = r'```dataview\nTABLE summary as "Summary", attendees as "Attendees"\nFROM "Meetings"\nWHERE date\(split\(transpired, " "\)\[0\]\) = date\(".{0,20}"\)\n```'

WORKOUT_REPLACEMENT = r'```dataview\nTABLE title as "Title", type as "Type"\nFROM #health OR #fitness AND !"Extras"\nWHERE date(transpired) = date("{props[created]}")\nOR date(created) = date("{props[created]}")\n```'

COMMUNITY_REPLACEMENT = r'## Community\n```dataview\nTABLE title as "Title", type as "Type"\nFROM #social AND !"Extras"\nWHERE date(transpired) = date("{props[created]}")\n```'

HOBBIES_REPLACEMENT = r'## Hobbies\n```dataview\nTABLE title as "Title", type as "Type"\nFROM #hobby AND !"Extras"\nWHERE date(transpired) = date("{props[created]}")\n```'

STATEMENT_REMOVE = "You could also revisit a random person `dice: #people|link` to see how they are doing. Relationships require effort from both sides, but initiation requires effort from you."


def fix_daily_notes(root_path):
    for file_path in common.gather_files(root_path):
        replace_learning = sap.replace_in_file(
            file_path,
            LEARNING_TABLE,
            COMMUNITY_REPLACEMENT,
            format_function=sap.format_on_property_values,
        )
        remove_reading = sap.remove_in_file(file_path, READING_TABLE)
        rename_workouts = sap.replace_in_file(
            file_path, "## Workouts", "## Health & Fitness", regex=False
        )
        workout_relacement = sap.replace_in_file(
            file_path,
            WORKOUT_TABLE,
            WORKOUT_REPLACEMENT,
            format_function=sap.format_on_property_values,
        )
        rename_meetings = sap.replace_in_file(
            file_path, "## Meetings", "## Hobbies", regex=False
        )
        replace_meetings = sap.replace_in_file(
            file_path,
            MEETINGS_TABLE,
            HOBBIES_REPLACEMENT,
            format_function=sap.format_on_property_values,
        )
        statement_remove = sap.remove_in_file(file_path, STATEMENT_REMOVE, regex=False)
        remove_duplicates = sap.file_remove_consecutive_duplicate_lines(file_path)
        clean_queries = sap.file_delete_newlines_before_queries(file_path)
        print(f"-------------{file_path}-------------")
        print(f"Replaced learning table: {replace_learning}")
        print(f"Removed Reading Table: {remove_reading}")
        print(f"Renamed Workouts to Health & Fitness: {rename_workouts}")
        print(f"Renamed Meetings to Hobbies: {rename_meetings}")
        print(f"Replaced Workouts table: {workout_relacement}")
        print(f"Replaced Meetings Table: {replace_meetings}")
        print(f"Removed random person: {statement_remove}")
        print(f"Removed duplicate lines: {remove_duplicates}")
        print(f"Cleaned query spacing: {clean_queries}")
        print("")


def main():
    root_path = BASE_PATH + "Testing/"
    fix_daily_notes(root_path)


if __name__ == "__main__":
    main()
