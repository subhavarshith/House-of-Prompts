events_log = []

def add_event(event):
    events_log.append(event)
    # Keep only last 50 events
    if len(events_log) > 50:
        events_log.pop(0)

def get_events():
    return events_log
