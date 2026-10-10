from datetime import date, datetime
from zoneinfo import ZoneInfo

SEMESTER_START_DATE = date(2026, 8, 31)
TZ = ZoneInfo("Europe/Kyiv")  

def get_current_week(date=None):
    if not date:
        date = datetime.now(TZ).date()

    if date < SEMESTER_START_DATE:
        return 0

    return (date - SEMESTER_START_DATE).days // 7 + 1