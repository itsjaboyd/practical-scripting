import pathlib
import common
import datetime
import json
import importlib

fm = importlib.import_module("front-matter")

MEETINGS_DIRECTORY = "/Users/jasonboyd/Tracking/Meetings/"
PEOPLE_DIRECTORY = "/Users/jasonboyd/Tracking/People/"
UPDATED_JSON = "/Users/jasonboyd/Tracking/Extras/Other/updated.json"


def update_contacted_automatic():
    root_path = common.get_path(MEETINGS_DIRECTORY)
    saved_meetings = common.get_updated_json(UPDATED_JSON)["meetings"]
    current_meetings = get_oldest_sorted_meetings(MEETINGS_DIRECTORY)
    update_meetings_list, total_results = [], []
    for meeting in current_meetings:
        if str(meeting) not in saved_meetings:
            update_meetings_list.append(meeting)
    for meeting in update_meetings_list:
        results = update_contacted_from_meeting(meeting)
        total_results.append((meeting, results))
    return total_results


def generate_updated_meetings_json():
    root_path = common.get_path(MEETINGS_DIRECTORY)
    updated_json = common.get_updated_json(UPDATED_JSON)
    meetings = get_oldest_sorted_meetings(MEETINGS_DIRECTORY)
    meetings = [str(m) for m in meetings]
    updated_json["meetings"] = meetings
    return common.write_updated_json(UPDATED_JSON, updated_json)


def update_contacted_overall():
    meetings = get_oldest_sorted_meetings(MEETINGS_DIRECTORY)
    total_results = []
    for meeting in meetings:
        results = update_contacted_from_meeting(meeting)
        total_results.append(results)
    return total_results


def get_oldest_sorted_meetings(root_path):
    meetings = common.gather_files(root_path)
    meetings.sort(key=lambda mt: fm.get_front_matter_value(mt, "transpired"))
    return meetings


def update_contacted_from_meeting(meeting_file):
    meeting_file = common.get_path(meeting_file)
    if not meeting_file.exists():
        return False
    results = []
    transpired = fm.get_front_matter_value(meeting_file, "transpired")
    for associate in get_people_associated(meeting_file):
        result = fm.update_front_matter(associate, "contacted", transpired)
        results.append((associate.name, result))
    return results


def get_people_associated(meeting_file):
    attendee_links = fm.get_front_matter_value(meeting_file, "attendees")
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
