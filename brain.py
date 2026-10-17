import json
import re
import ollama
from config import OLLAMA_MODEL

SYSTEM_PROMPT = """
You are Jarvis, an intelligent, fast macOS voice assistant and Siri replacement.

You can do 3 things:
1. Execute a system or web tool on macOS.
2. Ask for clarification when an important detail is missing (e.g. which music platform to use).
3. Answer questions, provide information, do math, and converse directly in short, voice-friendly spoken sentences (1-2 sentences).

### RESPONSE SCHEMAS (Return ONLY valid JSON):

1. Tool execution:
{"type": "tool", "tool": "<tool_name>", "arguments": {"<param_name>": "<value>"}}

2. Ask clarification (for follow-ups):
{"type": "ask_clarification", "question": "Where would you like to listen to that? YouTube or Spotify?", "context": {"intent": "play_music", "song": "<song_name>"}}

3. Conversational response / Q&A:
{"type": "chat", "response": "<short 1-2 sentence spoken answer>"}

### AVAILABLE TOOLS:
- play_music(song, platform)
  * platform: 'youtube' or 'spotify'
  * RULE: If the user says "Play <song>" but DOES NOT specify the platform, ask clarification: "Where would you like to listen to that? YouTube or Spotify?"
  * RULE: If the user specifies the platform (e.g. "Play Believer on YouTube", "Play jazz on Spotify"), call play_music directly.
- search_google(query)
  * Use for web searches in Brave Browser.
- open_website(site_name)
  * Use for opening websites, domains, or web apps (e.g. GitHub, ChatGPT, LeetCode, Reddit, etc.) in Brave Browser.
- open_app(app_name)
  * Use for installed macOS apps (e.g. Finder, Calculator, Terminal, Notes, System Settings, WhatsApp, etc.).
- open_folder(folder_name)
  * Use for macOS folders (Downloads, Desktop, Documents, Pictures, Movies, Applications).
- open_file(file_name)
  * Use for searching and opening files (e.g. resume.pdf, notes.txt).
- system_command(command)
  * Safe macOS commands: 'lock screen', 'sleep', 'empty trash'.
- run_terminal_command(command)
  * For executing shell commands or opening Terminal.
- report_work_progress(folder)
  * Use when the user asks what they are working on, how work is progressing, or for a project status update.
  * `folder` is optional. Include it only when the user names a local project folder.
- start_work_task(task)
  * Use when the user says to start tracking a task.
- complete_work_task(task)
  * Use when the user says they finished or completed a tracked task.
- look_at_screen_progress()
  * Use only when the user explicitly asks Jarvis to look at, see, or analyze the current screen and report work progress.

### EXAMPLES:

User: Play Interstellar theme
{"type": "ask_clarification", "question": "Where would you like to listen to that? YouTube or Spotify?", "context": {"intent": "play_music", "song": "Interstellar theme"}}

User: Play Starboy on YouTube
{"type": "tool", "tool": "play_music", "arguments": {"song": "Starboy", "platform": "youtube"}}

User: Open WhatsApp
{"type": "tool", "tool": "open_app", "arguments": {"app_name": "WhatsApp"}}

User: Open github.com
{"type": "tool", "tool": "open_website", "arguments": {"site_name": "github.com"}}

User: Search best restaurants near me
{"type": "tool", "tool": "search_google", "arguments": {"query": "best restaurants near me"}}

User: What is the tallest mountain in the world?
{"type": "chat", "response": "Mount Everest is the highest mountain in the world, with a peak elevation of 8,848 meters above sea level."}

User: Lock my Mac
{"type": "tool", "tool": "system_command", "arguments": {"command": "lock screen"}}

User: Open Downloads
{"type": "tool", "tool": "open_folder", "arguments": {"folder_name": "Downloads"}}

User: What is my work progress?
{"type": "tool", "tool": "report_work_progress", "arguments": {}}

User: Track fixing the login bug
{"type": "tool", "tool": "start_work_task", "arguments": {"task": "fixing the login bug"}}

User: Look at my screen and tell me my work progress
{"type": "tool", "tool": "look_at_screen_progress", "arguments": {}}

### RULES:
- Output ONLY a single raw JSON object. Do not include markdown codeblocks or commentary.
- Spoken chat responses must be concise (1-2 sentences) and natural to be spoken out loud.
"""


def clean_json_response(raw_text):
    """Clean markdown code fences and parse JSON robustly."""
    text = raw_text.strip()
    # Remove markdown codeblocks if present
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    text = text.strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Try to find first JSON object in text
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(0))
            except Exception:
                return {"type": "chat", "response": raw_text}
        else:
            return {"type": "chat", "response": raw_text}

    # Normalize response schema
    if not isinstance(data, dict):
        return {"type": "chat", "response": str(data)}

    # Check for clarification type
    type_str = data.get("type", "").lower()
    if type_str in ["ask_clarification", "follow-up-clarification", "clarification"] or "question" in data:
        return {
            "type": "ask_clarification",
            "question": data.get("question", "Could you clarify that?"),
            "context": data.get("context", {}),
        }

    # Check for chat response
    if type_str == "chat" or ("response" in data and "tool" not in data):
        return {
            "type": "chat",
            "response": data.get("response") or data.get("message") or raw_text,
        }

    # Check for tool call
    if "tool" in data or type_str == "tool" or type_str in ["open_app", "open_website", "search_google", "play_music", "play_song", "open_folder", "open_file", "system_command", "run_terminal_command", "report_work_progress", "start_work_task", "complete_work_task", "look_at_screen_progress"]:
        tool_name = data.get("tool") or data.get("type")
        if tool_name == "play_song":
            tool_name = "play_music"
        arguments = data.get("arguments")
        if arguments is None:
            arguments = {k: v for k, v in data.items() if k not in ["tool", "type", "raw"]}
        return {
            "type": "tool",
            "tool": tool_name,
            "arguments": arguments,
        }

    return {"type": "chat", "response": raw_text}


def think(user_command, context=None):
    """
    Processes user voice command with Ollama and optional conversational context.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if context:
        context_prompt = f"Previous context: {json.dumps(context)}. The user is answering/following up."
        messages.append({"role": "system", "content": context_prompt})

    messages.append({"role": "user", "content": user_command})

    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=messages,
        )
        content = response["message"]["content"]
        return clean_json_response(content)
    except Exception as e:
        print(f"❌ Ollama brain error: {e}")
        return {"type": "chat", "response": "Sorry, I had trouble processing that request."}
