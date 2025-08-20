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


LEARNING_TABLE = r'```dataview\n\s*TABLE updated as "Updated", title as "Title", summary as "Summary"\n\s*FROM "Subjects" OR "Courses"\n\s*WHERE file.mtime >= date\(".{0,20}"\) - dur\(\d day\)\n```'

READING_TABLE = r'## Reading Updates\n\n```dataview\n\s*TABLE title as "Publication", author as "Author", finished as "Finished\?"\n\s*FROM "Reading"\n\s*WHERE file.mtime >= date\(".{0,20}"\) - dur\(\d day\)\n```'

WORKOUT_TABLE = r'```dataview\n\s*TABLE type as "Workout Type", mood as "Overall Mood", effort as "Overall Effort"\s*\n\s*FROM "Fitness"\nWHERE file.ctime >= date\(".{0,20}"\) - dur\(\d day\)\n```'

MEETINGS_TABLE = r'```dataview\n\s*TABLE summary as "Summary", attendees as "Attendees", file.cday as "Cday"\n\s*FROM "Meetings"\n\s*WHERE file.cday = date\(".{0,20}"\)\n```'

REVISIT_TABLE = r'```dataview\n\s*TABLE contacted as "Last Contacted"\s*\n\s*FROM "People"\n\s*WHERE revisit = "True"\n\s*AND date\(contacted, "yyyy-MM-dd T"\) <= date\(".{0,20}"\) - dur\(\d month\)\n```'

WORKOUT_REPLACEMENT = r'```dataview\nTABLE title as "Title", type as "Type"\nFROM #health OR #fitness AND !"Extras"\nWHERE date(transpired) = date(this.created)\nOR date(created) = date(this.created)\n```'

COMMUNITY_REPLACEMENT = r'## Community\n```dataview\nTABLE title as "Title", type as "Type"\nFROM #social AND !"Extras"\nWHERE date(transpired) = date(this.created)\n```'

HOBBIES_REPLACEMENT = r'```dataview\nTABLE title as "Title", type as "Type"\nFROM #hobby AND !"Extras"\nWHERE date(transpired) = date(this.created)\n```'

STATEMENT_REMOVE = "You could also revisit a random person `dice: #people|link` to see how they are doing. Relationships require effort from both sides, but initiation requires effort from you."


def fix_daily_notes(root_path):
    for file_path in common.gather_files(root_path):
        remove_learning_header = sap.remove_in_file(file_path, "## Learning\n", regex=False)
        replace_learning = sap.replace_in_file(
            file_path,
            LEARNING_TABLE,
            COMMUNITY_REPLACEMENT,
            format_function=sap.format_on_property_values,
        )
        remove_learning_statement = sap.remove_in_file(
            file_path, "Put something you learned today here.", regex=False
        )
        remove_reading = sap.remove_in_file(file_path, READING_TABLE)
        remove_revisit_header = sap.remove_in_file(
            file_path, "## Revisit People\n", regex=False
        )
        remove_revisit_table = sap.remove_in_file(file_path, REVISIT_TABLE)
        rename_workouts = sap.replace_in_file(
            file_path, "## Workout Updates", "## Health & Fitness", regex=False
        )
        workout_relacement = sap.replace_in_file(
            file_path,
            WORKOUT_TABLE,
            WORKOUT_REPLACEMENT,
            format_function=sap.format_on_property_values,
        )
        rename_meetings = sap.replace_in_file(
            file_path, "## Meeting Updates", "## Hobbies", regex=False
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
        strip_file = common.file_strip_whitespace(file_path)
        print(f"\n-------------{file_path}-------------")
        print(f"Removed Learning Header: {remove_learning_header}")
        print(f"Replaced Learning Table: {replace_learning}")
        print(f"Removed Learning Statement: {remove_learning_statement}")
        print(f"Removed Reading Table: {remove_reading}")
        print(f"Removed Revisit Header: {remove_revisit_header}")
        print(f"Removed Revisit Table: {remove_revisit_table}")
        print(f"Renamed Workouts to Health & Fitness: {rename_workouts}")
        print(f"Renamed Meetings to Hobbies: {rename_meetings}")
        print(f"Replaced Workouts Table: {workout_relacement}")
        print(f"Replaced Meetings Table: {replace_meetings}")
        print(f"Removed Random Person: {statement_remove}")
        print(f"Removed Duplicate Lines: {remove_duplicates}")
        print(f"Cleaned Query Spacing: {clean_queries}")
        print(f"Stripped Whitespace: {strip_file}")
        print("")


def main():
    root_path = BASE_PATH + "Periodicals/Dailys/2024/July/"
    fix_daily_notes(root_path)


if __name__ == "__main__":
    main()
