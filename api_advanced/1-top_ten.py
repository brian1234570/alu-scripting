#!/usr/bin/python3
"""Prints the titles of the first 10 hot posts of a subreddit."""
import os
import requests


def get_token(client_id, secret, user_agent):
    """Return an OAuth access token, or None if it can't be obtained."""
    try:
        response = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=(client_id, secret),
            data={"grant_type": "client_credentials"},
            headers={"User-Agent": user_agent},
            timeout=10,
        )
        return response.json().get("access_token")
    except (requests.RequestException, ValueError):
        return None


def top_ten(subreddit):
    """Print the titles of the first 10 hot posts of a subreddit.

    Prints None if the subreddit is invalid or the request fails.
    """
    user_agent = "linux:alu-scripting:v1.0 (by /u/{})".format(
        os.environ.get("REDDIT_USERNAME", "anonymous"))
    headers = {"User-Agent": user_agent}
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    client_id = os.environ.get("REDDIT_CLIENT_ID")
    secret = os.environ.get("REDDIT_CLIENT_SECRET")
    if client_id and secret:
        token = get_token(client_id, secret, user_agent)
        if token:
            headers["Authorization"] = "bearer {}".format(token)
            url = "https://oauth.reddit.com/r/{}/hot".format(subreddit)

    try:
        response = requests.get(
            url,
            headers=headers,
            params={"limit": 10},
            allow_redirects=False,
            timeout=10,
        )
        if response.status_code != 200:
            print(None)
            return
        posts = response.json().get("data", {}).get("children", [])
    except (requests.RequestException, ValueError):
        print(None)
        return

    for post in posts:
        print(post.get("data", {}).get("title"))
