import os
import requests

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

CHANNEL_ID = "UCIPPMRA040LQr5QPyJEbmXA"

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
