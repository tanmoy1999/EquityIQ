from schemas.models import URL
from utilities.format import DateUtils
from core.constants import DATEFORMAT, HEADERS
from clients.nse import NSEClient
from clients.base import BaseHTTPClient


def main():
    # url = URL(DateUtils.format_date)
    url = URL(DATEFORMAT.DEFAULT)
    conn = NSEClient(url.generator, HEADERS)
    df = conn.get_data()
    print(df)


if __name__ == "__main__":
    main()