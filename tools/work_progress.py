"""Local, privacy-conscious work-progress reporting for Jarvis on macOS."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from config import VISION_MODEL


STATE_FILE = Path.home() / ".jarvis_work_progress.json"


def _run(command: list[str], timeout: int = 4) -> str:
    try:
        completed = subprocess.run(
            command, text=True, capture_output=True, timeout=timeout, check=False
        )
        return completed.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return ""


def _load_state() -> dict:
    try:
        return json.loads(STATE_FILE.read_text())
    except (OSError, json.JSONDecodeError):
        return {"tasks": []}


def _save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")


def _frontmost_app() -> tuple[str, str]:
    """Return the active app and its window title without reading screen content."""
    app = _run([
        "osascript", "-e",
        'tell application "System Events" to get name of first application process whose frontmost is true',
    ])
    if not app:
        return "an unknown application", ""

    title = _run([
        "osascript", "-e",
        'tell application "System Events" to tell first application process whose frontmost is true to get name of front window',
    ])
    return app, title


def _git_summary(folder: Optional[str]) -> str:
    if not folder:
        return ""
    path = Path(folder).expanduser()
    if not path.is_dir():
        return f"I could not find the folder {path}."

    root = _run(["git", "-C", str(path), "rev-parse", "--show-toplevel"])
    if not root:
        return f"{path.name} is not a Git project."

    status = _run(["git", "-C", root, "status", "--porcelain"])
    branch = _run(["git", "-C", root, "branch", "--show-current"]) or "detached HEAD"
    last_commit = _run(["git", "-C", root, "log", "-1", "--pretty=format:%s"])
    changed = len(status.splitlines()) if status else 0
    clean = "working tree is clean" if changed == 0 else f"{changed} changed file{'s' if changed != 1 else ''} not committed"
    message = f"In {Path(root).name} on {branch}, the {clean}."
    if last_commit:
        message += f" Last commit: {last_commit}."
    return message


def start_work_task(task: str) -> str:
    """Record a task that Jarvis can include in future progress reports."""
    task = task.strip()
    if not task:
        return "Tell me what task you want to start."
    state = _load_state()
    state.setdefault("tasks", []).append({
        "title": task,
        "status": "active",
        "started_at": datetime.now(timezone.utc).isoformat(),
    })
    _save_state(state)
    return f"Started: {task}."


def complete_work_task(task: str) -> str:
    """Mark the best matching active task complete."""
    wanted = task.strip().lower()
    state = _load_state()
    active = [item for item in state.get("tasks", []) if item.get("status") == "active"]
    match = next((item for item in active if wanted in item.get("title", "").lower()), None)
    if not match:
        return f"I could not find an active task matching {task}."
    match["status"] = "complete"
    match["completed_at"] = datetime.now(timezone.utc).isoformat()
    _save_state(state)
    return f"Completed: {match['title']}."


def report_work_progress(folder: Optional[str] = None) -> str:
    """Summarize active work context, tracked tasks, and optionally a Git project."""
    app, title = _frontmost_app()
    context = f"You are currently working in {app}"
    if title:
        context += f", window {title}"
    context += "."

    state = _load_state()
    active = [item["title"] for item in state.get("tasks", []) if item.get("status") == "active"]
    if active:
        task_summary = " Active tasks: " + "; ".join(active[:3]) + "."
        if len(active) > 3:
            task_summary += f" Plus {len(active) - 3} more."
    else:
        task_summary = " No tasks are currently being tracked."

    git = _git_summary(folder)
    return " ".join(part for part in [context, task_summary, git] if part)


def look_at_screen_progress() -> str:
    """Analyze the current display locally after the user explicitly asks for it."""
    handle, filename = tempfile.mkstemp(prefix="jarvis-screen-", suffix=".png")
    os.close(handle)
    screenshot = Path(filename)
    try:
        screenshot.unlink(missing_ok=True)
        capture = subprocess.run(
            ["screencapture", "-x", str(screenshot)],
            text=True, capture_output=True, timeout=15, check=False,
        )
        if capture.returncode != 0 or not screenshot.exists():
            return (
                "I could not see the screen. Give your terminal or Python Screen Recording "
                "permission in System Settings, then try again."
            )

        try:
            import ollama
        except ImportError:
            return "The Ollama Python package is not installed yet. Run pip install -r requirements.txt."

        response = ollama.chat(
            model=VISION_MODEL,
            messages=[{
                "role": "user",
                "content": (
                    "You are a privacy-conscious macOS work assistant. Describe only the user's "
                    "visible work progress in two concise spoken sentences: current task, evidence "
                    "of progress, and the most useful next step. Do not repeat sensitive text, "
                    "credentials, personal messages, or unrelated content."
                ),
                "images": [str(screenshot)],
            }],
        )
        answer = response.get("message", {}).get("content", "").strip()
        return answer or "I could see the screen, but I could not summarize the work progress."
    except subprocess.TimeoutExpired:
        return "Screen capture timed out. Please try again."
    except Exception as error:
        if "model" in str(error).lower() or "not found" in str(error).lower():
            return f"Install the local vision model first with: ollama pull {VISION_MODEL}."
        return "I could not analyze the screen. Check that Ollama is running and try again."
    finally:
        screenshot.unlink(missing_ok=True)
