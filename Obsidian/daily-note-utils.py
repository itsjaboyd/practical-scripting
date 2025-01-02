"""
    Commonly used utilities with daily note modification in Obsidian.

    Author: Jason Boyd
    Date: December 31, 2024
    Modified: January 1, 2025
"""

# TODO:
# * Add recursive option through note processing functions for directory processing
# * Provide unit testing alongside this module for practice
# * Provide formatting and clean comments as "production-ready" code
# * Possibly expand this code to provide "search and replace" functionality for notes

import datetime
import pathlib
import re

ISO_FORMAT_REGEX = r"[\d]{4}[-][\d]{2}[-][\d]{2}"
HEADER_INDEX = 8

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
    """Compile the supplied regex string and return a list of matches from a string."""

    matcher = re.compile(regexString)
    matches = matcher.finditer(matchString)
    foundMatches = [match for match in matches]
    return foundMatches

def updateDatesHandler(notePath, newDate, updateHeader=True):
    """Given a daily note, update its date variables to match the supplied date string."""
    newDate = extractDateObject(newDate)
    
    with open(notePath, "r+") as notePathFile:
        noteLines = notePathFile.readlines()
        for index in range(len(noteLines)):
            if index == HEADER_INDEX and updateHeader:
                noteLines[index] = newDate.strftime("# %A, %B %#d, %Y\n")

            for match in regexMatchesString(ISO_FORMAT_REGEX, noteLines[index]):
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

def flattenList(multiList, newlist):
    """Given a multi-dimensional list, flatten it for processing linearly."""

    for element in multiList:
        if isinstance(element, list):
            flattenList(element, newlist)
        else:
            newlist.append(element)
    return newlist

def processNoteDirectory(directory, recursive=False):
    """From a supplied directory, get all existing notes, optionally recursive."""

    notePaths = []
    if not isinstance(directory, pathlib.Path):
        raise ValueError(f"Supplied directory is not a Path object: {directory}.")
    if not directory.is_dir():
        raise TypeError(f"Supplied directory is not a directory: {directory}.")

    # return a list of all markdown files found in the directory
    return [str(noteFile.absolute()) for noteFile in directory.rglob("*.md")]

def processNoteString(noteString):
    """Given a note path string, return a list of paths, be it a file or directory."""
    
    noteList = []
    if isinstance(noteString, str):
        # could be a note file path or a directory
        objectPath = pathlib.Path(noteString)
        if objectPath.is_file():
            if objectPath.suffix != ".md": # not a markdown file
                raise TypeError(f"Supplied file is not a markdown (note) file: {objectPath.name}.")
            noteList.append(noteString)
        elif objectPath.is_dir():
            noteList.extend(processNoteDirectory(objectPath))
    return noteList

def getNotesList(noteObject):
    """Given a directory, list of notes, or single note, gather all markdown files."""

    noteList = []
    if isinstance(noteObject, str):
        noteList.extend(processNoteString(noteObject))
    elif isinstance(noteObject, list):
        # could be a list of note paths or list of directories
        flattenedList = flattenList(noteObject, [])
        if not all(isinstance(flatElement, str) for flatElement in flattenedList):
            raise TypeError(f"Cannot extract note paths from non-path objects: {noteObject}.")
        for noteElement in flattenedList:
            noteList.extend(processNoteString(noteElement))
    else: # user supplied a note object that cannot be processed
        raise ValueError(f"Cannot process supplied note object: {noteObject}.")
    return noteList

def updateDailyDates(noteObject, useFileNameDate=True, newDate=None, updateHeader=True, recursive=False):
    """Given a directory, list of notes, or single note, update the ISO dates in note body."""

    noteList = getNotesList(noteObject)

    for notePath in noteList:
        if useFileNameDate and newDate is not None:
            raise ValueError(f"Cannot use file date and supplied new date: {newDate}.")
        elif not useFileNameDate and newDate is None:
            raise ValueError(f"Cannot update notes without new date: {newDate}")
        elif useFileNameDate and newDate is None:
            newDate = pathlib.Path(notePath).name
        updateDatesHandler(notePath, newDate, updateHeader=updateHeader)