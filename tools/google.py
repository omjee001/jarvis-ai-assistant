import subprocess
import urllib.parse
from config import DEFAULT_BROWSER


def search_google(query):
    """
    Searches Google in Brave Browser.
    """
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}"

    try:
        subprocess.run([
            "open",
            "-a",
            DEFAULT_BROWSER,
            url,
        ], check=True)
    except subprocess.CalledProcessError:
        subprocess.run(["open", url])

    return f"Searching Google for '{query}'..."