import structlog
from langchain_core.tools import tool

from src.integrations.google_calendar import client
from src.integrations.google_calendar.exceptions import (
    GoogleCalendarError,
    GoogleCalendarNotConfiguredError,
)
from src.integrations.google_calendar.models import CalendarEvent

logger = structlog.get_logger(__name__)


def _format_event(e: CalendarEvent) -> str:
    if e.is_all_day:
        time_part = f"{e.start} (all day)"
    else:
        time_part = f"{e.start} – {e.end}"
    line = f"- [{e.event_id}] {e.summary} | {time_part}"
    if e.location:
        line += f" | {e.location}"
    if e.description:
        line += f"\n  {e.description[:200]}"
    return line


@tool(description=(
    "Get all calendar events for a specific day. "
    "Use when the user asks what they have planned on a particular date, "
    "or asks about their schedule today or tomorrow. "
    "date must be in YYYY-MM-DD format."
))
def get_daily_agenda(date: str) -> str:
    logger.info("Invoking get_daily_agenda tool", date=date)
    try:
        events = client.get_events_for_day(date)
        if not events:
            return f"No events found for {date}."
        return f"Events on {date}:\n" + "\n".join(_format_event(e) for e in events)
    except GoogleCalendarNotConfiguredError as e:
        return f"Google Calendar is not configured: {e.message}"
    except GoogleCalendarError as e:
        return f"Could not fetch agenda: {e.message}"


@tool(description=(
    "Get all calendar events for a 7-day window starting from start_date. "
    "Use when the user asks about their week, upcoming schedule, or plans for the next few days. "
    "start_date must be in YYYY-MM-DD format."
))
def get_weekly_agenda(start_date: str) -> str:
    logger.info("Invoking get_weekly_agenda tool", start_date=start_date)
    try:
        events = client.get_events_for_week(start_date)
        if not events:
            return f"No events found for the week starting {start_date}."
        return f"Events for the week of {start_date}:\n" + "\n".join(_format_event(e) for e in events)
    except GoogleCalendarNotConfiguredError as e:
        return f"Google Calendar is not configured: {e.message}"
    except GoogleCalendarError as e:
        return f"Could not fetch weekly agenda: {e.message}"


@tool(description=(
    "Search upcoming Google Calendar events by keyword. "
    "Use when the user asks about a specific recurring event by name, e.g. "
    "'when is my next therapy session', 'do I have a dentist appointment', "
    "'find my next flight'. Returns event IDs, titles, and times. "
    "max_results defaults to 10."
))
def search_calendar_events(query: str, max_results: int = 10) -> str:
    logger.info("Invoking search_calendar_events tool", query=query, max_results=max_results)
    try:
        events = client.search_events(query, max_results)
        if not events:
            return f"No upcoming events found matching '{query}'."
        return f"Upcoming events matching '{query}':\n" + "\n".join(_format_event(e) for e in events)
    except GoogleCalendarNotConfiguredError as e:
        return f"Google Calendar is not configured: {e.message}"
    except GoogleCalendarError as e:
        return f"Could not search events: {e.message}"


@tool(description=(
    "Create a new Google Calendar event. "
    "Use when the user asks to schedule, book, or add something to their calendar. "
    "start_datetime and end_datetime must be in ISO-8601 format: YYYY-MM-DDTHH:MM:SS. "
    "description and location are optional."
))
def create_calendar_event(
    summary: str,
    start_datetime: str,
    end_datetime: str,
    description: str | None = None,
    location: str | None = None,
) -> str:
    logger.info("Invoking create_calendar_event tool", summary=summary, start=start_datetime)
    try:
        event = client.create_event(summary, start_datetime, end_datetime, description, location)
        return f"Event created: [{event.event_id}] {event.summary} | {event.start} – {event.end}"
    except GoogleCalendarNotConfiguredError as e:
        return f"Google Calendar is not configured: {e.message}"
    except GoogleCalendarError as e:
        return f"Could not create event: {e.message}"


@tool(description=(
    "Delete a Google Calendar event by its event ID. "
    "Always call search_calendar_events or get_daily_agenda first to get the event ID. "
    "Always confirm with the user before deleting."
))
def delete_calendar_event(event_id: str) -> str:
    logger.info("Invoking delete_calendar_event tool", event_id=event_id)
    try:
        client.delete_event(event_id)
        return f"Event {event_id} deleted."
    except GoogleCalendarNotConfiguredError as e:
        return f"Google Calendar is not configured: {e.message}"
    except GoogleCalendarError as e:
        return f"Could not delete event: {e.message}"
