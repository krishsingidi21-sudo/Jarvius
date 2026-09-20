import os
import subprocess
from pathlib import Path


# =========================
# WINDOWS APPLICATIONS
# =========================

APPLICATIONS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "explorer": "explorer.exe",
    "file explorer": "explorer.exe",
    "command prompt": "cmd.exe",
    "cmd": "cmd.exe",
    "powershell": "powershell.exe",
    "paint": "mspaint.exe",
    "task manager": "taskmgr.exe",
    "control panel": "control.exe",
}


# =========================
# WINDOWS COMMAND
# =========================

def open_application(application_name):
    application_name = application_name.lower().strip()

    if application_name not in APPLICATIONS:
        return f"I don't know how to open {application_name}."

    try:
        subprocess.Popen(APPLICATIONS[application_name])
        return f"I opened {application_name}."

    except Exception as e:
        return f"I couldn't open {application_name}: {e}"


# =========================
# FOLDERS
# =========================

def open_folder(folder_path):
    folder_path = Path(folder_path)

    if not folder_path.exists():
        return f"The folder {folder_path} does not exist."

    if not folder_path.is_dir():
        return f"{folder_path} is not a folder."

    try:
        os.startfile(folder_path)
        return f"I opened the folder {folder_path}."

    except Exception as e:
        return f"I couldn't open the folder {folder_path}: {e}"


def create_folder(folder_path):
    folder_path = Path(folder_path)

    try:
        folder_path.mkdir(parents=True, exist_ok=True)
        return f"I created the folder {folder_path}."

    except Exception as e:
        return f"I couldn't create the folder {folder_path}: {e}"


# =========================
# FILE ACCESS
# =========================

SAFE_ROOT = Path(r"C:\Jarvius")


def is_safe_path(file_path):
    try:
        file_path = Path(file_path).resolve()
        safe_root = SAFE_ROOT.resolve()

        return file_path == safe_root or safe_root in file_path.parents

    except Exception:
        return False


def list_files(folder_path):
    folder_path = Path(folder_path)

    if not is_safe_path(folder_path):
        return "I can only access files and folders inside C:\\Jarvius."

    if not folder_path.exists():
        return f"The folder {folder_path} does not exist."

    if not folder_path.is_dir():
        return f"{folder_path} is not a folder."

    try:
        files = list(folder_path.iterdir())

        if not files:
            return f"The folder {folder_path} is empty."

        result = []

        for item in files:
            if item.is_dir():
                result.append(f"[Folder] {item.name}")
            else:
                result.append(f"[File] {item.name}")

        return "\n".join(result)

    except Exception as e:
        return f"I couldn't list the files: {e}"


def find_file(file_name, search_path=r"C:\Jarvius"):
    search_path = Path(search_path)

    if not is_safe_path(search_path):
        return "I can only search inside C:\\Jarvius."

    if not search_path.exists():
        return f"The folder {search_path} does not exist."

    try:
        matches = []

        for item in search_path.rglob("*"):
            if item.is_file() and item.name.lower() == file_name.lower():
                matches.append(str(item))

        if not matches:
            return f"I couldn't find {file_name}."

        return "\n".join(matches)

    except Exception as e:
        return f"I couldn't search for the file: {e}"


# =========================
# READ TEXT FILE
# =========================

ALLOWED_EXTENSIONS = {
    ".txt",
    ".md",
    ".csv",
    ".json",
    ".log",
    ".py",
    ".yaml",
    ".yml",
}

MAX_FILE_SIZE = 100 * 1024


def read_text_file(file_path):
    file_path = Path(file_path)

    if not is_safe_path(file_path):
        return "I can only read files inside C:\\Jarvius."

    if not file_path.exists():
        return f"The file {file_path} does not exist."

    if not file_path.is_file():
        return f"{file_path} is not a file."

    if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
        return f"I can't read {file_path.suffix} files."

    try:
        if file_path.stat().st_size > MAX_FILE_SIZE:
            return "That file is too large for me to read."

        return file_path.read_text(encoding="utf-8")

    except UnicodeDecodeError:
        return "I couldn't read that file because it is not a UTF-8 text file."

    except Exception as e:
        return f"I couldn't read the file: {e}"


# =========================
# TIME
# =========================

def get_time():
    from datetime import datetime

    current_time = datetime.now().strftime("%I:%M %p")

    return f"The current time is {current_time}."