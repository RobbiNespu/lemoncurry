from ago import human
from datetime import datetime


def ago(dt: datetime) -> str:
    # We have to convert the datetime we get to local time first, because ago
    # just strips the timezone from a timezone-aware datetime.
    dt = dt.astimezone()
    return human(dt, precision=1, past_tense='{}', abbreviate=True)
