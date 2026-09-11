import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

url  = "https://www.googleapis.com/youtube/v3/videos"
params = {
    "part": "snippet,statistics",
    "id":"dQw4w9WgXcQ",
    "key": API_KEY,
}

response = requests.get(url, params = params)
data = response.json()

print(response.status_code)
print(data["items"][0]["snippet"]["title"])

# Works! got a 200 status code and correct title - Sep 10, 2026