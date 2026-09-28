import csv
import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
if not API_KEY:
    raise SystemExit("YOUTUBE_API_KEY not found. Check your .env file.")

URL = "https://www.googleapis.com/youtube/v3/channels"
INPUT_PATH = "data/channels.csv"
OUTPUT_PATH = "data/channels_resolved.csv"

def resolve_handle(handle):
    params = {"part": "snippet,statistics", "forHandle": handle, "key": API_KEY}
    response = requests.get(URL, params=params, timeout=10)

    if response.status_code != 200:
        message = response.json()["error"]["message"]
        raise RuntimeError(f"API error for {handle}: {message}")

    items = response.json().get("items", [])
    if not items:
        return None

    channel = items[0]
    stats = channel["statistics"]
    return {
        "channel_id": channel["id"],
        "channel_name": channel["snippet"]["title"],
        "subscriber_count": stats.get("subscriberCount", ""),
        "video_count": stats.get("videoCount", ""),
    }

def main():
    with open(INPUT_PATH, newline="") as f:
        rows = list(csv.DictReader(f))

    not_found = []
    for row in rows:
        result = resolve_handle(row["channel_handle"])
        if result is None:
            not_found.append(row["channel_handle"])
        else:
            row.update(result)

    fieldnames = ["channel_handle", "channel_id", "channel_name", "niche",
                  "subscriber_count", "video_count", "notes"]
    with open(OUTPUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Resolved {len(rows) - len(not_found)} of {len(rows)} channels.")
    if not_found:
        print("Not found:", ", ".join(not_found))


if __name__ == "__main__":
    main()