# High-level obsidian note manipulation and modification

import datetime
import platform
import subprocess

if platform.system() == "Darwin":
    BASE_PATH = "/Users/jasonboyd/Tracking/"
else:  # use WSL's path to user notes on windows WSL
    BASE_PATH = "/mnt/c/Users/basonjoyd/Tracking/"

TEMPLATES_PATH = ""


def create_templated_note(template_name):
    pass


def open_daily_note():
    open_daily = "obsidian://daily?vault=Tracking"
    starter = "open" if platform.system() == "Darwin" else "start"
    result = subprocess.run([starter, open_daily], capture_output=True, text=True)
    return result


def gather_interval_files(start, end):
    pass


def gather_popular_files(root_path):
    pass


def build_vault_statistics(root_path):
    pass
