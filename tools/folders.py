import subprocess
import os

FOLDERS = {
    "desktop": os.path.expanduser("~/Desktop"),
    "downloads": os.path.expanduser("~/Downloads"),
    "documents": os.path.expanduser("~/Documents"),
    "pictures": os.path.expanduser("~/Pictures"),
    "movies": os.path.expanduser("~/Movies"),
    "applications": "/Applications",
}

def open_folder(folder_name):
    folder = folder_name.lower().strip()

    if folder not in FOLDERS:
        return f"I couldn't find the folder '{folder_name}'."

    subprocess.run(["open", FOLDERS[folder]])

    return f"Opening {folder_name}."