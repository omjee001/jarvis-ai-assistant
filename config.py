import os

# Assistant Configuration
ASSISTANT_NAME = "Jarvis"
DEFAULT_BROWSER = "Brave Browser"
OLLAMA_MODEL = "llama3.2"
# Install with: ollama pull llama3.2-vision
# This is used only after an explicit "look at my screen" request.
VISION_MODEL = "llama3.2-vision"
WAKE_WORD = "hey jarvis"

# Audio Recording & STT Settings
SAMPLE_RATE = 16000
BLOCK_SIZE = 1024
START_THRESHOLD = 0.015
SILENCE_THRESHOLD = 0.010
SILENCE_DURATION = 0.8
MAX_DURATION = 8

# Common macOS Directories
DEFAULT_SEARCH_FOLDERS = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Pictures"),
    os.path.expanduser("~/Movies"),
]

COMMON_FOLDERS = {
    "desktop": os.path.expanduser("~/Desktop"),
    "downloads": os.path.expanduser("~/Downloads"),
    "documents": os.path.expanduser("~/Documents"),
    "pictures": os.path.expanduser("~/Pictures"),
    "movies": os.path.expanduser("~/Movies"),
    "applications": "/Applications",
}

# Popular Websites Directory
POPULAR_WEBSITES = {
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
    "chatgpt": "https://chatgpt.com",
    "google": "https://www.google.com",
    "reddit": "https://www.reddit.com",
    "stackoverflow": "https://stackoverflow.com",
    "netflix": "https://www.netflix.com",
    "amazon": "https://www.amazon.com",
    "twitter": "https://twitter.com",
    "x": "https://x.com",
    "linkedin": "https://www.linkedin.com",
    "gmail": "https://mail.google.com",
    "spotify": "https://open.spotify.com",
}
