import pathlib
import common
import datetime
import json
import platform
import importlib

properties = importlib.import_module("properties")

if platform.system() == "Darwin":
    BASE_PATH = "/Users/jasonboyd/Tracking/"
else:  # use WSL's path to user notes on windows WSL
    BASE_PATH = "/mnt/c/Users/basonjoyd/Tracking/"

MEETINGS_DIRECTORY = BASE_PATH + "Meetings/"
PEOPLE_DIRECTORY = BASE_PATH + "People/"
UPDATED_JSON = BASE_PATH + "Extras/Other/meetings.json"


def update_contacted_automatic():
    root_path = common.get_path(MEETINGS_DIRECTORY)
    saved_meetings = common.get_updated_json(UPDATED_JSON)["meetings"]
    current_meetings = get_oldest_sorted_meetings(MEETINGS_DIRECTORY)
    update_meetings_list, total_results = [], []
    for meeting in current_meetings:
        truncated_meeting = str(meeting).replace(MEETINGS_DIRECTORY, "")
        if truncated_meeting not in saved_meetings:
            update_meetings_list.append(meeting)
    for meeting in update_meetings_list:
        results = update_contacted_from_meeting(meeting)
        total_results.append((meeting, results))
    update_meetings = generate_updated_meetings_json()
    return total_results


def generate_updated_meetings_json():
    root_path = common.get_path(MEETINGS_DIRECTORY)
    base_json = {"meetings": []}
    meetings = get_oldest_sorted_meetings(MEETINGS_DIRECTORY)
    meetings = [str(m).replace(MEETINGS_DIRECTORY, "") for m in meetings]
    base_json["meetings"] = meetings
    return common.write_updated_json(UPDATED_JSON, base_json)


def update_contacted_overall():
    meetings = get_oldest_sorted_meetings(MEETINGS_DIRECTORY)
    total_results = []
    for meeting in meetings:
        results = update_contacted_from_meeting(meeting)
        total_results.append(results)
    return total_results


def get_oldest_sorted_meetings(root_path):
    meetings = common.gather_files(root_path)
    meetings.sort(key=lambda mt: properties.get_property_value(mt, "transpired"))
    return meetings


def update_contacted_from_meeting(meeting_file):
    meeting_file = common.get_path(meeting_file)
    if not meeting_file.exists():
        return False
    results = []
    transpired = properties.get_property_value(meeting_file, "transpired")
    for associate in get_people_associated(meeting_file):
        result = properties.update_property(associate, "contacted", transpired)
        results.append((associate.name, result))
    return results


def get_people_associated(meeting_file):
    attendee_links = properties.get_property_value(meeting_file, "attendees")
    if attendee_links is None:
        return []
    attendees = common.sanitize_person_links(attendee_links)
    return get_people_notes(attendees)


def get_people_notes(person_names):
    if not isinstance(person_names, list):
        person_names = [person_names]
    person_paths = []
    person_names = [f"{pn}.md" for pn in person_names]
    everyone = common.gather_files(PEOPLE_DIRECTORY)
    for person in everyone:
        if person.name in person_names:
            person_paths.append(person)
    return person_paths
