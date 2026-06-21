import httplib2
import structlog
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import google_auth_httplib2
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.config.settings import settings
from src.integrations.google_calendar.exceptions import (
    GoogleCalendarError,
    GoogleCalendarNotConfiguredError,
)
from src.integrations.google_calendar.models import CalendarEvent

logger = structlog.get_logger(__name__)


class GoogleCalendarClient:

    def __init__(self):
        self._service = None

    def _get_service(self):
        if self._service is not None:
            return self._service

        if not all([
            settings.google_client_id,
            settings.google_client_secret,
            settings.google_refresh_token,
        ]):
            raise GoogleCalendarNotConfiguredError(
                "Google Calendar credentials are not configured. "
                "Set GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_REFRESH_TOKEN."
            )

        creds = Credentials(
            token=None,
            refresh_token=settings.google_refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.google_client_id,
            client_secret=settings.google_client_secret,
        )
        creds.refresh(Request())
        authed_http = google_auth_httplib2.AuthorizedHttp(
            creds, http=httplib2.Http(timeout=30)
        )
        self._service = build("calendar", "v3", http=authed_http, cache_discovery=False)
        return self._service

    def _tz(self) -> ZoneInfo:
        return ZoneInfo(settings.google_calendar_timezone)

    def _parse_event(self, raw: dict) -> CalendarEvent:
        start_raw = raw["start"].get("dateTime") or raw["start"].get("date")
        end_raw = raw["end"].get("dateTime") or raw["end"].get("date")
        is_all_day = "date" in raw["start"] and "dateTime" not in raw["start"]

        if is_all_day:
            start_fmt = start_raw
            end_fmt = end_raw
        else:
            start_dt = datetime.fromisoformat(start_raw).astimezone(self._tz())
            end_dt = datetime.fromisoformat(end_raw).astimezone(self._tz())
            start_fmt = start_dt.strftime("%Y-%m-%d %H:%M")
            end_fmt = end_dt.strftime("%H:%M")

        return CalendarEvent(
            event_id=raw["id"],
            summary=raw.get("summary", "(No title)"),
            start=start_fmt,
            end=end_fmt,
            description=raw.get("description"),
            location=raw.get("location"),
            is_all_day=is_all_day,
        )

    def get_events_for_day(self, date_str: str) -> list[CalendarEvent]:
        tz = self._tz()
        start = datetime.fromisoformat(f"{date_str}T00:00:00").replace(tzinfo=tz)
        end = start + timedelta(days=1)
        try:
            result = self._get_service().events().list(
                calendarId="primary",
                timeMin=start.isoformat(),
                timeMax=end.isoformat(),
                singleEvents=True,
                orderBy="startTime",
            ).execute()
        except HttpError as e:
            raise GoogleCalendarError(f"API error fetching day events: {e}") from e
        return [self._parse_event(e) for e in result.get("items", [])]

    def get_events_for_week(self, start_date_str: str) -> list[CalendarEvent]:
        tz = self._tz()
        start = datetime.fromisoformat(f"{start_date_str}T00:00:00").replace(tzinfo=tz)
        end = start + timedelta(days=7)
        try:
            result = self._get_service().events().list(
                calendarId="primary",
                timeMin=start.isoformat(),
                timeMax=end.isoformat(),
                singleEvents=True,
                orderBy="startTime",
            ).execute()
        except HttpError as e:
            raise GoogleCalendarError(f"API error fetching week events: {e}") from e
        return [self._parse_event(e) for e in result.get("items", [])]

    def search_events(self, query: str, max_results: int = 10) -> list[CalendarEvent]:
        from datetime import timezone as _tz_utc
        now = datetime.now(tz=_tz_utc.utc).isoformat()
        try:
            result = self._get_service().events().list(
                calendarId="primary",
                timeMin=now,
                q=query,
                singleEvents=True,
                orderBy="startTime",
                maxResults=max_results,
            ).execute()
        except HttpError as e:
            raise GoogleCalendarError(f"API error searching events: {e}") from e
        return [self._parse_event(e) for e in result.get("items", [])]

    def create_event(
        self,
        summary: str,
        start_datetime: str,
        end_datetime: str,
        description: str | None = None,
        location: str | None = None,
    ) -> CalendarEvent:
        body: dict = {
            "summary": summary,
            "start": {
                "dateTime": start_datetime,
                "timeZone": settings.google_calendar_timezone,
            },
            "end": {
                "dateTime": end_datetime,
                "timeZone": settings.google_calendar_timezone,
            },
        }
        if description:
            body["description"] = description
        if location:
            body["location"] = location
        try:
            raw = self._get_service().events().insert(
                calendarId="primary", body=body
            ).execute()
        except HttpError as e:
            raise GoogleCalendarError(f"API error creating event: {e}") from e
        return self._parse_event(raw)

    def update_event(
        self,
        event_id: str,
        summary: str | None = None,
        start_datetime: str | None = None,
        end_datetime: str | None = None,
        description: str | None = None,
        location: str | None = None,
    ) -> CalendarEvent:
        service = self._get_service()
        try:
            raw = service.events().get(calendarId="primary", eventId=event_id).execute()
        except HttpError as e:
            if e.resp.status == 404:
                raise GoogleCalendarError(f"Event '{event_id}' not found.") from e
            raise GoogleCalendarError(f"API error fetching event: {e}") from e

        if summary is not None:
            raw["summary"] = summary
        if description is not None:
            raw["description"] = description
        if location is not None:
            raw["location"] = location
        if start_datetime is not None:
            raw["start"] = {"dateTime": start_datetime, "timeZone": settings.google_calendar_timezone}
        if end_datetime is not None:
            raw["end"] = {"dateTime": end_datetime, "timeZone": settings.google_calendar_timezone}

        try:
            updated = service.events().update(
                calendarId="primary", eventId=event_id, body=raw
            ).execute()
        except HttpError as e:
            raise GoogleCalendarError(f"API error updating event: {e}") from e
        return self._parse_event(updated)

    def delete_event(self, event_id: str) -> None:
        try:
            self._get_service().events().delete(
                calendarId="primary", eventId=event_id
            ).execute()
        except HttpError as e:
            if e.resp.status == 404:
                raise GoogleCalendarError(f"Event '{event_id}' not found.") from e
            raise GoogleCalendarError(f"API error deleting event: {e}") from e