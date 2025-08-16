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

SEARCHABLE = """## Journaling

You are currently journaling for the month of [[Journal/2025/July|July]]. Write down what emotions you experienced today, the events that occurred, things you would like to reflect on when you review the day sometime in the future.

## Learning

%%daily-learning%%

```dataview
TABLE title as "Title", summary as "Summary"
FROM "Subjects" OR "Courses"
WHERE contains(flat(list(updated)), date("2025-07-31"))
```

## Reading

```dataview
	TABLE title as "Publication", author as "Author", finished as "Finished"
	FROM "Reading"
	WHERE contains(flat(list( updated )), date("2025-07-31"))
```

## Workouts

```dataview
TABLE type as "Workout Type", mood as "Overall Mood", effort as "Overall Effort" 
FROM "Fitness"
WHERE date(split(transpired, " ")[0]) = date("2025-07-31")
```

## Meetings

```dataview
	TABLE summary as "Summary", attendees as "Attendees"
	FROM "Meetings"
	WHERE date(split(transpired, " ")[0]) = date("2025-07-31")
```

You could also revisit a random person `dice: #people|link` to see how they are doing. Relationships require effort from both sides, but initiation requires effort from you."""


learning = """## Learning

%%daily-learning%%

```dataview
TABLE title as "Title", summary as "Summary"
FROM "Subjects" OR "Courses"
WHERE contains(flat(list(updated)), date("2025-07-30"))
```"""

LEARNING_TABLE = r'## Learning\n\n.*\n\n```dataview\nTABLE title as "Title", summary as "Summary"\nFROM "Subjects" OR "Courses"\nWHERE contains\(flat\(list\(updated\)\), date\(".{0,20}"\)\)\n```'



def main():
    results = sap.is_in_files(BASE_PATH + "Periodicals/Dailys/", LEARNING_TABLE)
    #daily = BASE_PATH + "Periodicals/Dailys/2025/July/2025-07-31.md"
    #contents = common.read_file_contents(daily)
    #print(repr(contents))
    #print(sap.is_in_file(daily, LEARNING_REGEX))
    for el in results:
        if not el[-1]:
            print(el)




if __name__ == "__main__":
    main()
