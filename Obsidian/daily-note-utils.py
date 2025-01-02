"""
    Commonly used utilities with daily note modification in Obsidian.

    Author: Jason Boyd
    Date: December 31, 2024
    Modified: January 1, 2025
"""

# TODO:
# * Provide unit testing alongside this module for practice
# * Provide formatting and clean comments as "production-ready" code
# * Possibly expand this code to provide "search and replace" functionality for notes

import datetime
import pathlib
import re

ISO_FORMAT_REGEX = r"[\d]{4}[-][\d]{2}[-][\d]{2}"
HEADER_INDEX = 8


def extractDateObject(dateObject):
    """Attempt to create a pathlib.Path() object from the supplied dateObject.

    Args:
        dateObject (str): should exist as the ISO-format for conversion: YYYY-MM-DD
        dateObject (int): should exist as a timestamp for conversion: i.e. 1735853336
        dateObject (None): If dateObject is None, the function will use today's date

    Raises:
        ValueError: raised if supplied argument is not of type str, int, or None.

    Returns:
        pathlib.Path: converted from the supplied dateObject argument.
    """

    convertDate = None
    if isinstance(dateObject, str):
        convertDate = datetime.date.fromisoformat(dateObject)
    elif isinstance(dateObject, int):
        convertDate = datetime.date.fromtimestamp(dateObject)
    elif isinstance(dateObject, datetime.date):
        convertDate = dateObject
    elif dateObject is None:
        convertDate = datetime.date.today()

    if convertDate is None:
        raise ValueError(f"Cannot extract date from date object: {dateObject}")
    return convertDate


def flattenList(multiList, newlist):
    """Given a multi-dimensional list, flatten it for processing linearly."""

    for element in multiList:
        if isinstance(element, list):
            flattenList(element, newlist)
        else: # add the non-list element to the newList
            newlist.append(element)
    return newlist


def getNotesList(noteObject, recursively):
    """Given a directory, list of notes, or single note, gather all markdown files."""

    noteList = []
    if isinstance(noteObject, str):
        noteList.extend(processNoteString(noteObject, recursively))
    elif isinstance(noteObject, list):
        flattenedList = flattenList(noteObject, [])
        if not all(isinstance(flatElement, str) for flatElement in flattenedList):
            raise TypeError(f"Cannot extract note paths from non-path objects: {noteObject}.")
        for noteElement in flattenedList:
            noteList.extend(processNoteString(noteElement, recursively))
    else: # user supplied a note object that cannot be processed
        raise ValueError(f"Cannot process supplied note object: {noteObject}.")
    return noteList


def processNoteDirectory(directory, recursively):
    """From a supplied directory, get all existing notes, optionally recursively."""

    if not isinstance(directory, pathlib.Path):
        raise ValueError(f"Supplied directory is not a Path object: {directory}.")
    if not directory.is_dir():
        raise TypeError(f"Supplied directory is not a directory: {directory}.")
    
    # return a list of all markdown files found, optionally recursively
    pathObjects = directory.rglob("*.md") if recursively else directory.glob("*.md")
    return [str(noteFile.absolute()) for noteFile in pathObjects]


def processNoteString(noteString, recursively):
    """Given a note path string, return a list of paths, be it a file or directory."""
    
    noteList = []
    if isinstance(noteString, str):
        objectPath = pathlib.Path(noteString)
        if objectPath.is_file():
            if objectPath.suffix != ".md":
                raise TypeError(f"Supplied file is not a markdown (note) file: {objectPath.name}.")
            noteList.append(noteString)
        elif objectPath.is_dir():
            noteList.extend(processNoteDirectory(objectPath, recursively))
    return noteList


def regexMatchesString(regexString, matchString):
    """Compile the supplied regex string and return a list of matches from a string."""

    matcher = re.compile(regexString)
    matches = matcher.finditer(matchString)
    foundMatches = [match for match in matches]
    return foundMatches


def replaceLineMatches(lineString, index, newDate, updateHeader):
    """Given a string line, replace its ISO format dates with newDate and other updates."""

    if index == HEADER_INDEX and updateHeader:
        return newDate.strftime("# %A, %B %#d, %Y\n")

    updatedString = lineString
    for match in regexMatchesString(ISO_FORMAT_REGEX, lineString):
        inputDate = newDate.isoformat()
        dayNavigation = ""
        try: # attempt to get any additional information about day links
            dayNavigation = lineString[match.end():match.end() + 10]
        except IndexError as ie:
            pass

        conversion = {"|yesterday": 1, "|tomorrow'": -1}
        if any(key in dayNavigation for key in conversion.keys()):
            correctDate = newDate - datetime.timedelta(days=conversion[dayNavigation])
            inputDate = correctDate.isoformat()
        updatedString = updatedString.replace(match.group(), inputDate, 1)
    return updatedString


def updateDailyDates(noteObject, newDate=None, updateHeader=True, recursively=False):
    """Given a directory, list of notes, or single note, update the ISO dates in note body."""

    noteList = getNotesList(noteObject, recursively)
    for notePath in noteList:
        useDate = pathlib.Path(notePath).stem if newDate is None else newDate
        updateDatesHandler(notePath, useDate, updateHeader=updateHeader)


def updateDatesHandler(notePath, newDate, updateHeader):
    """Given a daily note, update its date variables to match the supplied date string."""
    newDate = extractDateObject(newDate)
    
    with open(notePath, "r+") as notePathFile:
        noteLines = notePathFile.readlines()
        for index in range(len(noteLines)):
            noteLines[index] = replaceLineMatches(noteLines[index], index, newDate, updateHeader)
        # put the index at beginning, clear the file, and write the new lines
        notePathFile.seek(0)
        notePathFile.truncate(0)
        notePathFile.writelines(noteLines)