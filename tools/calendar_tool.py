from langchain.tools import Tool
from calendar_integration.calendar_handler import get_upcoming_events, create_event
import datetime
import dateparser

def calendar_summary(_=None):
    return get_upcoming_events()

def calendar_create(input_text: str) -> str:
    """Parses input like 'tomorrow at 16:00 to call Kalix'."""
    parsed_time = dateparser.parse(input_text, settings={"TIMEZONE": "Europe/Berlin"})
    if not parsed_time:
        return "Sorry, I couldn't understand the date/time in your input."

    # Extract intent/summary from input_text
    parts = input_text.split(" to ", 1)
    summary = parts[1] if len(parts) > 1 else "Untitled Event"

    return create_event(summary=summary, start_time=parsed_time)

calendar_tools = [
    Tool.from_function(
        name="CalendarCreate",
        description="Use to create calendar events. Input: 'Tomorrow at 14:00, dentist appointment'.",
        func=calendar_create
    ),
    Tool.from_function(
        name="CalendarSummary",
        description="Use to view upcoming events in the next few days.",
        func=calendar_summary
    )
]

