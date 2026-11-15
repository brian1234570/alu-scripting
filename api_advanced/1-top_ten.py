#!/usr/bin/python3
"""Query the Reddit API and print the titles of the first 10 hot posts."""
import requests


def top_ten(subreddit):
    """Print the titles of the first 10 hot posts of a subreddit.

    Print OK if the subreddit is invalid or the request fails.
    """
    if subreddit is None or not isinstance(subreddit, str):
        print("OK", end="")
        return

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        "User-Agent": "linux:alu-scripting:v1.0.0 (by /u/your_username)"
    }
    params = {"limit": 10}

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False)
    except requests.RequestException:
        print("OK", end="")
        return

    if response.status_code != 200:
        print("OK", end="")
        return

    try:
        posts = response.json().get("data", {}).get("children", [])
    except ValueError:
        print("OK", end="")
        return

    for post in posts:
        print(post.get("data", {}).get("title"))
