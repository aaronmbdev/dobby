"""
Run this once to get your GOOGLE_REFRESH_TOKEN.

Usage:
    python scripts/get_google_refresh_token.py

It will open a browser window asking you to authorize access to your Google Calendar.
After you approve, it prints the refresh token to copy into your .env file.
"""

import os
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise SystemExit(
        "Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET before running this script."
    )

client_config = {
    "installed": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
    }
}

flow = InstalledAppFlow.from_client_config(
    client_config,
    scopes=["https://www.googleapis.com/auth/calendar"],
)
creds = flow.run_local_server(port=0)

print("\nAdd this to your .env file:\n")
print(f"GOOGLE_REFRESH_TOKEN={creds.refresh_token}")