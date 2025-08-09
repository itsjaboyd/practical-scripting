import importlib
import common

fm = importlib.import_module("front-matter")


def main():
    multiline = """
## Meetings
```dataview
TABLE
FROM "People"
WHERE this.fm is in that.fm
SORT file.ctime DESC

"""
    print(repr(multiline))


if __name__ == "__main__":
    main()
