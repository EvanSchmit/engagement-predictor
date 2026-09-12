# YouTube Engagement Predictor

Predicting video engagement from metadata using the YouTube Data API v3.
Collects channels and video metadata, engineers features, and compares classification models.

## Setup

Requires a YouTube Data API v3 key.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a ".env" file in the project root: