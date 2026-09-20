import os
import subprocess
from pathlib import Path


# =========================
# APPLICATIONS
# =========================

APPLICATIONS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "explorer": "explorer.exe",
}


def open_application(application_name):
    application_name = application_name.lower().strip()

    if application_name not in APPLICATIONS:
        return f"I don't have permission to open {application_name}."

    try:
        subprocess.Popen(APPLICATIONS[application_name])
        return f"I opened {application_name}."

    except Exception as e:
        return f"I couldn't open {application_name}: {e}"


# =========================
# FOLDERS
# =========================

def open_folder(folder_path):
    try:
        path = Path(folder_path).expanduser().resolve()

        if not path.exists():
            return f"The folder {path} does not exist."

        os.startfile(path)

        return f"I opened {path}."

    except Exception as e:
        return f"I couldn't open the folder: {e}"


# =========================
# CREATE FOLDER
# =========================

def create_folder(folder_path):
    try:
        path = Path(folder_path).expanduser().resolve()

        path.mkdir(parents=True, exist_ok=True)

        return f"I created the folder {path}."

    except Exception as e:
        return f"I couldn't create the folder: {e}"


# =========================
# WINDOWS COMMAND
# =========================

def get_time():
    from datetime import datetime

    current_time = datetime.now().strftime("%I:%M %p")

    return f"The current time is {current_time}."