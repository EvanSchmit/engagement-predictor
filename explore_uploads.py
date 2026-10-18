import os
import requests
import json

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

CHANNEL_ID = "UCIPPMRA040LQr5QPyJEbmXA"

def duration_to_seconds(duration):
    """Convert an ISO 8601 duration like "PT53S" to total seconds"""
    if not duration.startswith("PT"):
        raise ValueError(f"Unsupported duration: {duration}")
    rest = duration[2:]

    hours = 0
    if "H" in rest:
        hours_text, rest = rest.split("H")
        hours = int(hours_text)
    minutes = 0
    if "M" in rest:
        minutes_text, rest = rest.split("M")
        minutes = int(minutes_text)
    seconds = 0
    if "S" in rest:
        seconds_text, rest = rest.split("S")
        seconds = int(seconds_text)

    return hours * 3600 + minutes * 60 + seconds

    
uploads_playlist_id = "UU" + CHANNEL_ID[2:]
print(uploads_playlist_id)

URL = "https://www.googleapis.com/youtube/v3/playlistItems"

params = {
    "part": "contentDetails",
    "playlistId": uploads_playlist_id,
    "maxResults": 50,
    "key": API_KEY,
}

video_ids = []

while True:
    response = requests.get(URL, params=params, timeout=10)
    data = response.json()
    for item in data["items"]:
        video_ids.append(item["contentDetails"]["videoId"])

    if "nextPageToken" not in data:
        break
    params["pageToken"] = data["nextPageToken"]

print(len(video_ids))

VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"

videos = []
for start in range(0, len(video_ids), 50):
    batch = video_ids[start:start + 50]
    video_params = {
        "part": "snippet,statistics,contentDetails",
        "id": ",".join(batch),
        "key": API_KEY,
    }
    response = requests.get(VIDEOS_URL, params=video_params, timeout=10)
    videos_data = response.json()

    for item in videos_data["items"]:
        stats = item["statistics"]
        videos.append({
            "video_id": item["id"],
            "title": item["snippet"]["title"],
            "published_at": item["snippet"]["publishedAt"],
            "duration_s": duration_to_seconds(item["contentDetails"]["duration"]),
            "view_count": int(stats["viewCount"]),
            "like_count": int(stats["likeCount"]) if "likeCount" in stats else None,
            "comment_count": int(stats["commentCount"]) if "commentCount" in stats else None,
        })

print(len(video_ids), len(videos))

SHORTS_MAX_SECONDS = 180

shorts = []
for v in videos:
    if v["duration_s"] <= SHORTS_MAX_SECONDS:
        shorts.append(v)
print(len(shorts))