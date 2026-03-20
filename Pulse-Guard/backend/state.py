from typing import List, Dict, Any
from .models.telemetry import EventLogEntry

events_log: List[Dict[str, Any]] = []

def add_event(event: Dict[str, Any]) -> None:
    """Adds a new event to the in-memory log, keeping only the last 50."""
    events_log.append(event)
    if len(events_log) > 50:
        events_log.pop(0)

def get_events() -> List[Dict[str, Any]]:
    """Returns the list of stored events."""
    return events_log
