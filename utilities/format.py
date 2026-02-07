from datetime import datetime, date
from core.constants import DATEFORMAT

class DateUtils:
    format_date = date.today().strftime(DATEFORMAT.DATE_STANDARD)
    format_datetime = date.today().strftime(DATEFORMAT.DATETIME_STANDARD)

    def extract_date(col: str) -> str:
        """
        Docstring for extract_date
        
        :param col: Description
        :type col: str
        :return: Description
        :rtype: str
        """
        date_part = col.replace("change_", "").split("_")[0]
        return f"{date_part[4:8]}-{date_part[2:4]}-{date_part[0:2]}"
