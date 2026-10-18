import os
import sqlite3
from datetime import datetime, timezone
import csv

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

DB_PATH = "data/youtube.db"
PLAYLIST_URL = "https://www.googleapis.com/youtube/v3/playlistItems"
VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"
MAX_VIDEOS_PER_CHANNEL = 100
CHANNELS_PATH = "data/channels_resolved.csv"

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

def get_video_ids(channel_id: str) -> list[str]:
    """Return up to 100 IDs of uploads on a channel."""
    params = {
        "part": "contentDetails",
        "playlistId": "UU" + channel_id[2:],
        "maxResults": 50,
        "key": API_KEY,
    }
    video_ids = []

    while True:
        response = requests.get(PLAYLIST_URL, params=params, timeout=10)
        if response.status_code != 200:
            message = response.json()["error"]["message"]
            raise RuntimeError(f"Playlist error for {channel_id}: {message}")
        data = response.json()
        for item in data["items"]:
            video_ids.append(item["contentDetails"]["videoId"])

        if len(video_ids) >= MAX_VIDEOS_PER_CHANNEL:
            break

        if "nextPageToken" not in data:
            break
        params["pageToken"] = data["nextPageToken"]

    return video_ids[:MAX_VIDEOS_PER_CHANNEL]

def get_video_details(channel_id: str, video_ids: list[str]) -> list[dict]:
    """Fetch details for a channel's videos and return one record per video."""
    collected_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    videos = []

    for start in range(0, len(video_ids), 50):
        batch = video_ids[start:start + 50]
        params = {
            "part": "snippet,statistics,contentDetails",
            "id": ",".join(batch),
            "key": API_KEY,
        }
        response = requests.get(VIDEOS_URL, params=params, timeout=10)
        if response.status_code != 200:
            message = response.json()["error"]["message"]
            raise RuntimeError(f"Videos error for {channel_id}: {message}")

        for item in response.json()["items"]:
            if item["snippet"]["liveBroadcastContent"] != "none":
                continue
            stats = item["statistics"]
            videos.append({
                "video_id": item["id"],
                "channel_id": channel_id,
                "title": item["snippet"]["title"],
                "published_at": item["snippet"]["publishedAt"],
                "duration_s": duration_to_seconds(item["contentDetails"]["duration"]),
                "view_count": int(stats["viewCount"]),
                "like_count": int(stats["likeCount"]) if "likeCount" in stats else None,
                "comment_count": int(stats["commentCount"]) if "commentCount" in stats else None,
                "collected_at": collected_at,
            })

    return videos

def save_videos(conn: sqlite3.Connection, videos: list[dict]) -> None:
    """Insert or update video records, then commit."""
    conn.executemany("""
        INSERT OR REPLACE INTO videos (
            video_id, channel_id, title, published_at, duration_s,
            view_count, like_count, comment_count, collected_at
        ) VALUES (
            :video_id, :channel_id, :title, :published_at, :duration_s,
            :view_count, :like_count, :comment_count, :collected_at
        )
    """, videos)
    conn.commit()

def create_table(conn: sqlite3.Connection) -> None:
    """Create the videos table if it doesn't exist yet."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            video_id      TEXT PRIMARY KEY NOT NULL,
            channel_id    TEXT NOT NULL,
            title         TEXT,
            published_at  TEXT,
            duration_s    INTEGER,
            view_count    INTEGER,
            like_count    INTEGER,
            comment_count INTEGER,
            collected_at  TEXT
        )
    """)
    conn.commit()

def main():
    with open(CHANNELS_PATH, newline="") as f:
        channels = list(csv.DictReader(f))

    conn = sqlite3.connect(DB_PATH)
    create_table(conn)

    for channel in channels:
        channel_id = channel["channel_id"]
        video_ids = get_video_ids(channel_id)
        videos = get_video_details(channel_id, video_ids)
        save_videos(conn, videos)
        print(f"{channel['channel_name']}: saved {len(videos)} videos")

    conn.close()


if __name__ == "__main__":
    main()