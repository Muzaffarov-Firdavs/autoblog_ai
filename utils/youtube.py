import os, html
from googleapiclient.discovery import build

def search_video_embed(topic: str) -> str:
    """
    Return an <iframe> embed code for the top-ranked YouTube video
    that matches the topic. Requires YOUTUBE_API_KEY in .env
    """
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise RuntimeError("YOUTUBE_API_KEY missing from .env")

    yt = build("youtube", "v3", developerKey=api_key, cache_discovery=False)
    resp = yt.search().list(
        part="snippet",
        q=topic,
        type="video",
        relevanceLanguage="en",
        maxResults=1,
        safeSearch="moderate"
    ).execute()

    items = resp.get("items", [])
    if not items:
        raise RuntimeError("No YouTube results found")

    video_id = items[0]["id"]["videoId"]
    title    = html.escape(items[0]["snippet"]["title"])

    return (
        f'<iframe width="560" height="315" '
        f'src="https://www.youtube.com/embed/{video_id}" '
        f'title="{title}" frameborder="0" '
        'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
        'allowfullscreen></iframe>'
    )
