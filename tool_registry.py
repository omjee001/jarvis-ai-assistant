from tools.apps import open_app
from tools.browser import open_website
from tools.google import search_google
from tools.music import play_music
from tools.folders import open_folder
from tools.files import open_file
from tools.system import system_command
from tools.terminal import run_terminal_command
from tools.work_progress import (
    complete_work_task,
    look_at_screen_progress,
    report_work_progress,
    start_work_task,
)

TOOLS = {
    "open_app": {
        "function": open_app,
        "description": "Open an installed macOS application",
    },
    "open_website": {
        "function": open_website,
        "description": "Open a website or domain in Brave Browser",
    },
    "search_google": {
        "function": search_google,
        "description": "Search Google in Brave Browser",
    },
    "play_song": {
        "function": play_music,
        "description": "Search and play a song on YouTube (direct first video autoplay) or Spotify",
    },
    "play_music": {
        "function": play_music,
        "description": "Search and play a song on YouTube or Spotify",
    },
    "open_folder": {
        "function": open_folder,
        "description": "Open a macOS folder",
    },
    "open_file": {
        "function": open_file,
        "description": "Search and open a file by name",
    },
    "system_command": {
        "function": system_command,
        "description": "Execute macOS system commands like lock screen, sleep, empty trash",
    },
    "run_terminal_command": {
        "function": run_terminal_command,
        "description": "Run a shell/terminal command or open the terminal",
    },
    "report_work_progress": {
        "function": report_work_progress,
        "description": "Report the active macOS work context, tracked tasks, and optional Git project status",
    },
    "start_work_task": {
        "function": start_work_task,
        "description": "Start tracking a named work task",
    },
    "complete_work_task": {
        "function": complete_work_task,
        "description": "Mark a named tracked work task complete",
    },
    "look_at_screen_progress": {
        "function": look_at_screen_progress,
        "description": "Capture and locally analyze the current screen after an explicit user request",
    },
}
