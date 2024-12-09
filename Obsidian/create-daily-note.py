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

# all static global variables that will not change or are calculated at runtime with args
DAILYS_PATH = "C:\\Users\\jason\\Personal-Notes\\Dailys\\"
TEMPLATE_DAILYS_PATH = "C:\\Users\\jason\\Personal-Notes\\Extras\\Templates\\daily-note.md"
LOGGING_FILE = "C:\\Users\\jason\\Development\\Logs\\Obsidian\\create-daily-note.log"
DETERMINER = "transpired"

# caller supplied all three required paths for note creation so use args
if len(sys.argv) == 4:
    DAILYS_PATH = sys.argv[1]
    TEMPLATE_DAILYS_PATH = sys.argv[2]
    LOGGING_FILE = sys.argv[3]

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

    # 1. preliminary check to ensure the script has real file and path locations
    checkPathsExist([DAILYS_PATH, TEMPLATE_DAILYS_PATH, LOGGING_FILE])

    # 2. check to make sure there is no currently existing daily note
    checkDailyExists(createdDailysPath)

    # 3. copy the template file and move it into current daily path
    copyPath = copyNote(TEMPLATE_DAILYS_PATH, currentDailysPath)

    # 4. rename the file from the template name to its current daily name
    renameDailyNote(copyPath, createdDailysPath, createdNoteName)

    # 5. sanitize the daily note of extraneous dashes used in template
    sanitizeDailyNote(createdDailysPath, DETERMINER, createdNoteName)

    # log a final success message to the logging file
    logger.info(f"Creation of daily note {createdNoteName} completed.")

def checkPathsExist(pathList):
    """Check to make sure all supplied paths in pathList exist."""

    allExist = True
    for path in pathList:
        if not os.path.exists(path):
            allExist = False
            break
    if not allExist:
        logger.warning("Required paths do not exist, aborting!")
        sys.exit(1)

def checkDailyExists(dailyPath):
    """Check to ensure the daily note doesn't already exist and exit if it does."""

    if os.path.exists(dailyPath):
        logger.warning("Today's daily note already exists, aborting!")
        sys.exit(2)

def copyNote(targetFile, destDirectory):
    """Copy the targetFile to a destDirectory and exit if it fails."""

    copied, copyPath, message = False, None, ""
    try: # attempt to copy the targetFile to a destDirectory
        copyPath = shutil.copy(targetFile, destDirectory)
    except FileNotFoundError as fnfe:
        if not os.path.exists(targetFile):
            message = f"Cannot copy a non-existent template note: {targetFile}"
        elif not os.path.exists(destDirectory):
            logger.info(f"Destination directory {destDirectory} will be created for this note.")
            os.makedirs(destDirectory)
            copyPath = shutil.copy(targetFile, destDirectory)
            message = f"Successfully copied template to created directory: {destDirectory}"
            copied = True
        else: # some other uncaught FileNotFoundError that occurred
            message = f"Failed to copy template: {fnfe}"
    except:
        message = "Failed to copy template due to an exception."
    else: # there were no exceptions with the copy attempt
        copied = True
        message = f"Successfully copied template note to dailys directory: {destDirectory}."
    if not copied:
        logger.error(message)
        sys.exit(3)
    logger.info(message)
    return copyPath

def renameDailyNote(notePath, newName, noteName):
    """Rename the given file notePath to newName and exit if it fails."""

    renamed, message = False, ""
    try: # attempt to rename the note path to today's note name
        os.rename(notePath, newName)
    except FileExistsError:
        message = "File already exists, cannot rename."
    except FileNotFoundError:
        message = "Supplied note path not found, cannot rename."
    except:
        message = "Failed to rename due to an exception."
    else: # there were no exceptions with the rename attempt
        renamed = True
        message = f"Successfully renamed template to daily note {noteName}."
    if not renamed:
        logger.error(message)
        sys.exit(3)
    logger.info(message)

def sanitizeDailyNote(notePath, determiner, noteName):
    """Open the notePath and modify select lines that match the determiner."""

    if not os.path.exists(notePath):
        logger.error(f"Cannot sanitize non-existent note {notePath}.")
        sys.exit(5)

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