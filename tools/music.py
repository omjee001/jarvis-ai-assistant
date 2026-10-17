import os
import subprocess
import urllib.parse
from config import DEFAULT_BROWSER
from tools.youtube import play_song as play_youtube_top_video


def is_app_installed(app_name):
    """Check if an application exists in standard macOS application paths."""
    system_path = f"/Applications/{app_name}.app"
    user_path = os.path.expanduser(f"~/Applications/{app_name}.app")
    return os.path.exists(system_path) or os.path.exists(user_path)


def play_spotify(song):
    """Play song on Spotify app if installed, or fallback to Brave browser."""
    encoded_song = urllib.parse.quote(song)

    if is_app_installed("Spotify"):
        try:
            # Open Spotify desktop app and search
            subprocess.run(["open", f"spotify:search:{encoded_song}"], check=True)
            # Try AppleScript to tell Spotify to play
            applescript = """
            tell application "Spotify"
                activate
                delay 1
                play
            end tell
            """
            subprocess.run(["osascript", "-e", applescript], check=False)
            return f"Playing '{song}' on Spotify."
        except Exception:
            pass

    # Fallback to browser
    web_url = f"https://open.spotify.com/search/{encoded_song}"
    try:
        subprocess.run(["open", "-a", DEFAULT_BROWSER, web_url], check=True)
    except subprocess.CalledProcessError:
        subprocess.run(["open", web_url])
    return f"Opening Spotify in Brave for '{song}'."


def play_music(song, platform="youtube"):
    """
    Unified music handler. Routes playback to the requested platform.
    Supported platforms: 'youtube', 'spotify', 'youtube music'.
    """
    platform_clean = (platform or "youtube").lower().strip()

    if "spotify" in platform_clean:
        return play_spotify(song)
    elif "youtube music" in platform_clean or "yt music" in platform_clean:
        encoded = urllib.parse.quote_plus(song)
        url = f"https://music.youtube.com/search?q={encoded}"
        try:
            subprocess.run(["open", "-a", DEFAULT_BROWSER, url], check=True)
        except subprocess.CalledProcessError:
            subprocess.run(["open", url])
        return f"Opening YouTube Music in Brave for '{song}'."
    else:
        # Default to YouTube first-video auto-play
        return play_youtube_top_video(song)
