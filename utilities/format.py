from datetime import datetime, date
from core.constants import DATEFORMAT

class DateUtils:
    format_date = date.today().strftime(DATEFORMAT.DATE_STANDARD)
    format_datetime = date.today().strftime(DATEFORMAT.DATETIME_STANDARD)
