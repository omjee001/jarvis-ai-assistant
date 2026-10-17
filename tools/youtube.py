import subprocess
import urllib.parse
import re
import requests
from config import DEFAULT_BROWSER

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


def find_top_youtube_video(query):
    """
    Finds the first video URL for a given search query on YouTube.
    Uses fast regex parsing with yt-dlp as a fallback.
    """
    encoded_query = urllib.parse.quote_plus(query)
    search_url = f"https://www.youtube.com/results?search_query={encoded_query}"

    # 1. Fast HTML regex approach (< 1 second)
    try:
        resp = requests.get(search_url, headers=HEADERS, timeout=4)
        if resp.status_code == 200:
            # Extract video IDs matching standard 11-char pattern
            video_ids = re.findall(r"/watch\?v=([a-zA-Z0-9_-]{11})", resp.text)
            if video_ids:
                # Find first unique video ID
                for vid in video_ids:
                    if len(vid) == 11:
                        return f"https://www.youtube.com/watch?v={vid}"
    except Exception as e:
        print(f"Direct YouTube search failed: {e}")

    # 2. yt-dlp fallback
    try:
        import yt_dlp
        ydl_opts = {
            "quiet": True,
            "extract_flat": True,
            "default_search": "ytsearch1",
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)
            if "entries" in info and len(info["entries"]) > 0:
                first_entry = info["entries"][0]
                video_url = first_entry.get("url") or f"https://www.youtube.com/watch?v={first_entry.get('id')}"
                return video_url
    except Exception as e:
        print(f"yt-dlp search failed: {e}")

    # 3. Fallback to YouTube search page if specific video can't be resolved
    return search_url


def play_song(song):
    """
    Resolves the top YouTube match for the requested song/video and opens it directly in Brave Browser.
    """
    print(f"🔍 Searching top YouTube video for: {song}...")
    video_url = find_top_youtube_video(song)

    try:
        subprocess.run([
            "open",
            "-a",
            DEFAULT_BROWSER,
            video_url,
        ], check=True)
    except subprocess.CalledProcessError:
        # If specified browser fails, open in default system browser
        subprocess.run(["open", video_url])

    if "watch?v=" in video_url:
        return f"Playing the top result for '{song}' on YouTube."
    else:
        return f"Searching YouTube for '{song}'."