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


def flattenList(multiList, newlist=[]):
    """Given a multi-dimensional list, flatten it for processing linearly.

    Args:
        multiList (list): the multidimensional list to flatten.
        newList (list): the starting list to add elements from multiList into.

    Returns:
        list: the flattened list that is one-dimensional, containing all elements.
    """

    for element in multiList:
        if isinstance(element, list):
            flattenList(element, newlist)
        else: # add the non-list element to the newList
            newlist.append(element)
    return newlist


def getNotesList(noteObject, recursively):
    """Given a directory, list of notes, or single note, gather all markdown files.

    Args:
        noteObject (str): a directory or note file string to process and add to noteList.
        noteObject (list): a list of directories or note files to process and add to notelist.
        recursively (bool): optional boolean flag to find all notes in subdirectories.

    Raises:
        TypeError: if noteObject is a (multidimensional) list and elements are not strings.
        ValueError: if noteObject is something other than a string or list.

    Returns:
        list: a list of gathered markdown file notes found from the supplied noteObject.
    """

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
    """From a supplied directory, get all existing notes, optionally recursively.

    Args:
        directory (str): a stinrg directory to gather markdown notes from.
        recursively (bool): optionally recursively gather notes in subdirectories.

    Raises:
        ValueError: if directory is not a pathlib.Path object.
        TypeError: if directory is not actually a directory.

    Returns:
        list: the list of all found markdown (.md) notes from directory
    """

    if not isinstance(directory, pathlib.Path):
        raise ValueError(f"Supplied directory is not a Path object: {directory}.")
    if not directory.is_dir():
        raise TypeError(f"Supplied directory is not a directory: {directory}.")
    
    # return a list of all markdown files found, optionally recursively
    pathObjects = directory.rglob("*.md") if recursively else directory.glob("*.md")
    return [str(noteFile.absolute()) for noteFile in pathObjects]


def processNoteString(noteString, recursively):
    """Given a note path string, return a list of paths, be it a file or directory.

    Args:
        noteString (str): the note string object used to process note files from, 
            could be a directory or a note file itself.
        recursively (bool): optionally gather notes in subdirectories when processing
            the noteString object, passed from calling function to process functions.

    Raises:
        TypeError: if the noteString is a note path, but not a mardown note file.

    Returns:
        list: a list to iterate over that contains all found notes from processing
            the noteString object, optionally recursively for subdirectories.
    """
    
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
    """Compile the supplied regex string and return a list of matches from a string.

    Args:
        regexString (str): the regex matcher to compile and find matches with.
        matchString (str): the actual string to find matches in using regex.

    Returns:
        list: the list of found matches within the string from regex matches. 
            Since python re.finditer() returns an interable and not a list, 
            the function returns a list for typical list properties and functions.
    """

    matcher = re.compile(regexString)
    matches = matcher.finditer(matchString)
    foundMatches = [match for match in matches]
    return foundMatches


def replaceLineMatches(lineString, index, newDate, updateHeader):
    """Given a string line, replace its ISO format dates with newDate and other updates.

    Args:
        lineString (str): just a string to replace found matches with newDate.
        index (int): the index from a line in a note file used for checks and header updates.
        newDate (pathlib.Path): the date to replace matches with in the lineString.
        updateHeader (bool): update the daily note header with a strftime date.

    Returns:
        str: the updated lineString with replaced newDate ISO date matches.
    """

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
    """Given a directory, list of notes, or single note, update the ISO dates in note body.

    Args:
        noteObject (any): object denoting a string directory, note path, or list to process.
        newDate (any, optional): an optional new date to replace ISO date matches with; 
            strings should be supplied as ISO formatted (YYYY-MM-DD). Defaults to None.
        updateHeader (bool, optional): flag to update the daily note header with the 
            supplied newDate in a strftime output. Defaults to True.
        recursively (bool, optional): update notes in found subdirectories. Defaults to False.
    """

    noteList = getNotesList(noteObject, recursively)
    for notePath in noteList:
        useDate = pathlib.Path(notePath).stem if newDate is None else newDate
        updateDatesHandler(notePath, useDate, updateHeader=updateHeader)


def updateDatesHandler(notePath, newDate, updateHeader):
    """Given a daily note, update its ISO date matches to match the supplied newDate.
        This function will open the file, read its lines and overwrite with all 
        processed new lines.

    Args:
        notePath (str): the note path string to open and write to.
        newDate (any): the new date to replace matches with.
        updateHeader (bool): update the daily note header with the newDate.
    """
    newDate = extractDateObject(newDate)
    
    with open(notePath, "r+") as notePathFile:
        noteLines = notePathFile.readlines()
        for index in range(len(noteLines)):
            noteLines[index] = replaceLineMatches(noteLines[index], index, newDate, updateHeader)
        # put the index at beginning, clear the file, and write the new lines
        notePathFile.seek(0)
        notePathFile.truncate(0)
        notePathFile.writelines(noteLines)