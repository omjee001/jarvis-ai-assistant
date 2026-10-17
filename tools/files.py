import os
import subprocess

SEARCH_FOLDERS = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Pictures"),
]


def open_file(file_name):
    target = file_name.lower().strip()

    for folder in SEARCH_FOLDERS:
        if not os.path.exists(folder):
            continue

        for root, _, files in os.walk(folder):
            for file in files:
                if file.lower() == target:
                    path = os.path.join(root, file)
                    subprocess.run(["open", path])
                    return f"Opening {file}"

    return f"I couldn't find '{file_name}'."