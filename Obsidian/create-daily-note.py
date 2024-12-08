"""""
    Create Obsidian's daily note feature automatically using a scheduled 
    task and this Python script. When daily notes are forgotten to be 
    made, the manual process of plugging in correct dates is just lame. 
    This script automatically copies and throws it into the correct Dailys 
    folder in the Obsidian vault.

    Author: Jason Boyd
    Date: December 5, 2024
    Modified: December 6, 2024
"""""

import os
import sys
import datetime
import shutil
import logging

# all static global variables that will not change or are calculated at runtime
DAILYS_PATH = "/Users/jasonboyd/Notes/Dailys/"
TEMPLATE_DAILYS_PATH = "/Users/jasonboyd/Notes/Extras/Templates/daily-note.md"
LOGGING_FILE = "/Users/jasonboyd/Development/Logs/Obsidian/create-daily-note.log"
DETERMINER = "transpired"


# logging creation for logging purposes as this script will run automatically
logger = logging.getLogger("create-daily-note")
logging.basicConfig(
    filename=LOGGING_FILE,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)

def main():
    """Perform all steps required to create today's daily note."""

    # all date specific variables that are calculated at runtime
    today = datetime.date.today()
    currentDailysPath = os.path.join(DAILYS_PATH, f"{today.year}/{today.strftime('%B')}/")
    createdDailysPath = os.path.join(currentDailysPath, today.isoformat() + ".md")
    createdNoteName = os.path.split(createdDailysPath)[-1]

    # 1. check to make sure there is no currently existing daily note
    checkExists(createdDailysPath)

    # 2. copy the template file and move it into current daily path
    copyPath = copyNote(TEMPLATE_DAILYS_PATH, currentDailysPath)

    # 3. rename the file from the template name to its current daily name
    renameDailyNote(copyPath, createdDailysPath, createdNoteName)

    # 4. sanitize the daily note of extraneous dashes used in template
    sanitizeDailyNote(createdDailysPath, DETERMINER, createdNoteName)

    # 5. log a final success message to the logging file
    logger.info(f"Creation of daily note {createdNoteName} completed.")

def checkExists(dailyPath):
    """Check to ensure the daily note doesn't already exist and exit if it does."""

    if os.path.exists(dailyPath):
        logger.warning("Today's daily note already exists, aborting!")
        sys.exit(1)

def copyNote(targetFile, destDirectory):
    """Copy the targetFile to a destDirectory and exit if it fails."""

    status = {"copied": False, "copyPath": None, "message": ""}
    try: # attempt to copy the targetFile to a destDirectory
        copyPath = shutil.copy(targetFile, destDirectory)
        status["copyPath"] = copyPath
    except FileNotFoundError:
        status["message"] = f"Cannot copy a non-existent template note: {targetFile}"
    except:
        status["message"] = "Failed to copy template due to an exception."
    else: # there were no exceptions with the copy attempt
        status["copied"] = True
        status["message"] = f"Successfully copied template note to dailys directory: {destDirectory}."
    if not status["copied"]:
        logger.error(status['message'])
        sys.exit(2)
    logger.info(status["message"])
    return copyPath

def renameDailyNote(notePath, newName, noteName):
    """Rename the given file notePath to newName and exit if it fails."""

    status = {"renamed": False, "message": ""}
    try: # attempt to rename the note path to today's note name
        os.rename(notePath, newName)
    except FileExistsError:
        status["message"] = "File already exists, cannot rename."
    except FileNotFoundError:
        status["message"] = "Supplied note path not found, cannot rename."
    except:
        status["message"] = "Failed to rename due to an exception."
    else: # there were no exceptions with the rename attempt
        status["renamed"] = True
        status["message"] = f"Successfully renamed template to daily note {noteName}."
    if not status["renamed"]:
        logger.error(status['message'])
        sys.exit(3)
    logger.info(status["message"])

def sanitizeDailyNote(notePath, determiner, noteName):
    """Open the notePath and modify select lines that match the determiner."""

    if not os.path.exists(notePath):
        logger.error(f"Cannot sanitize non-existent note {notePath}.")
        sys.exit(4)

    with open(notePath, "r+") as notePathFile:
        noteLines = notePathFile.readlines()
        # trim all lines by a character that include determiner.
        for index in range(len(noteLines)):
            if determiner in noteLines[index]:
                noteLines[index] = noteLines[index][:-2] + "\n"
        notePathFile.seek(0)
        notePathFile.truncate(0)
        notePathFile.writelines(noteLines)
    logger.info(f"Successfully sanitized daily note {noteName}.")
    
if __name__ == "__main__":
    main()
