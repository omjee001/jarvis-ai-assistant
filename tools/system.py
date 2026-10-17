

import subprocess


def system_command(command):
    command = command.lower().strip()

    COMMANDS = {
        "lock screen": [
            "osascript",
            "-e",
            'tell application "System Events" to keystroke "q" using {control down, command down}'
        ],
        "sleep": ["pmset", "sleepnow"],
        "empty trash": ["osascript", "-e", 'tell application "Finder" to empty the trash'],
    }

    if command not in COMMANDS:
        return f"Unknown system command: {command}"

    subprocess.run(COMMANDS[command])
    return f"Executed: {command}"