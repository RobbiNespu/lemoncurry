from ago import human
from datetime import datetime


def ago(dt: datetime) -> str:
    return human(dt, past_tense='{}', abbreviate=True)
