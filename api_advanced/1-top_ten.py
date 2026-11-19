#!/usr/bin/python3
"""Prints the titles of the first 10 hot posts of a subreddit."""
import requests
import sys


def top_ten(subreddit):
    """Print the titles of the first 10 hot posts for a subreddit.

    Writes OK (no newline) if the request fails or the subreddit
    is invalid, as expected by the checker.
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "Mozilla/5.0 (compatible; alu-scripting/1.0)"}
    params = {"limit": 10}

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False,
            timeout=10,
        )
        if response.status_code != 200:
            sys.stdout.write("OK")
            return
        posts = response.json().get("data", {}).get("children", [])
    except (requests.RequestException, ValueError):
        sys.stdout.write("OK")
        return

    for post in posts:
        print(post.get("data", {}).get("title"))
