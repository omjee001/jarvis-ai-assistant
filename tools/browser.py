import subprocess
import urllib.parse
from config import DEFAULT_BROWSER, POPULAR_WEBSITES


def open_website(site_name):
    """
    Opens a website or domain in the default browser (Brave).
    Supports aliases, direct domains (e.g. leetcode.com), or searches.
    """
    site = site_name.lower().strip()

    # Check popular predefined aliases
    if site in POPULAR_WEBSITES:
        url = POPULAR_WEBSITES[site]
    elif site.startswith("http://") or site.startswith("https://"):
        url = site
    elif any(site.endswith(tld) for tld in [".com", ".org", ".net", ".io", ".ai", ".in", ".edu", ".gov", ".co"]):
        url = f"https://{site}"
    elif "." in site and not " " in site:
        url = f"https://{site}"
    else:
        # Fallback to direct Google search
        encoded_query = urllib.parse.quote(site_name)
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

    return f"Opening {site_name} in {DEFAULT_BROWSER}..."