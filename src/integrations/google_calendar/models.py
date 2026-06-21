from dataclasses import dataclass


@dataclass(frozen=True)
class CalendarEvent:
    event_id: str
    summary: str
    start: str
    end: str
    description: str | None
    location: str | None
    is_all_day: bool
