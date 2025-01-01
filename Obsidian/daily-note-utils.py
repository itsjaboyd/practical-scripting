"""
    Commonly used utilities with daily note modification in Obsidian.

    Author: Jason Boyd
    Date: December 31, 2024
    Modified: December 31, 2024
"""

import datetime
import re

ISO_DATE_REGEX = r"[\d]{4}[-][\d]{2}[-][\d]{2}"

def extractDateObject(dateObject):
    """Return a datetime.date object from the supplied date object."""

    convertDate = None
    if isinstance(dateObject, str):
        try: # attempt to extract date from iso string
            convertDate = datetime.date.fromisoformat(dateObject)
        except ValueError as ve:
            print(f"Unable to convert date from string ISO: {ve}")
        except TypeError as te:
            print(f"Unable to convert date from numbered date: {te}")
    elif isinstance(dateObject, int):
        try: # attempt to extract date from timestamp value
            convertDate = datetime.date.fromtimestamp(dateObject)
        except ValueError as ve:
            print(f"Unable to convert date from timestamp: {ve}")
    elif isinstance(dateObject, datetime.date):
        print(f"Supplied date object is already a date object: {dateObject}")
        convertDate = dateObject
    elif dateObject is None:
        convertDate = datetime.date.today()
        print(f"Supplied date was None, using today's date: {convertDate}")

    if convertDate is None:
        raise ValueError(f"Cannot extract date from date object: {dateObject}")
    return convertDate

def regexMatchesString(regexString, matchString):

    matcher = re.compile(regexString)
    matches = matcher.finditer(matchString)
    foundMatches = [match for match in matches]
    return foundMatches

def updateTemplateDatesHandler(notePath, newDate, updateHeader=True):
    """Given a daily note, update its date variables to match the supplied date string."""
    newDate = extractDateObject(newDate)
    
    with open(notePath, "r+") as notePathFile:
        noteLines = notePathFile.readlines()
        for index in range(len(noteLines)):
            if index == HEADER_INDEX and updateHeader:
                noteLines[index] = newDate.strftime("# %A, %B %#d, %Y\n")

            for match in mregexMatchString(ISO_FORMAT_REGEX):
                inputDate = newDate.isoformat()
                dayNavigation = ""
                try: # attempt to get any additional information about day links
                    dayNavigation = noteLines[index][match.end():match.end() + 10]
                except IndexError as ie:
                    pass

                conversion = {"|yesterday": 1, "|tomorrow'": -1}
                if any(key in dayNavigation for key in conversion.keys()):
                    correctDate = newDate - datetime.timedelta(days=conversion[dayNavigation])
                    inputDate = correctDate.isoformat()
                noteLines[index] = noteLines[index].replace(match.group(), inputDate, 1)
        
        # put the index at beginning, clear the file, and write the new lines
        notePathFile.seek(0)
        notePathFile.truncate(0)
        notePathFile.writelines(noteLines)

def getNotePaths(directory, recursive=False):
    """From a supplied directory, get all existing notes, optionally recursive."""
    pass

def updateDailyDates(noteObject, useFilenameDate=True, newDate=None, updateHeader=True):
    """Given a directory, list of notes, or single note, update the ISO dates in note body."""

    noteIterable = []
    if isinstance(noteObject, str):
        # could be a note file path or a directory
    elif isinstance(noteObject, list)
        # could be a list of note paths or list of directories
    else: # user supplied invalid note object type for processing
        raise ValueError(f"Cannot update notes from note object: {noteObject}.")

    for notePath in noteIterable:
        if useFileNameDate and newDate is not None:
            newDate = extractDateObject(newDate)
        elif useFileNameDate and newDate is None:
            newDate = None # get the file name from the path
        elif not useFileNameDate and newDate is None:
            raise ValueError(f"Cannot update notes without new date: {newDate}")
        updaetTemplateDatesHandler(notePath, newDate, updateHeader=updateHeader)

def main():
    pass

if __name__ == "__main__":
    main()
