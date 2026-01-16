from schemas.models import URL
from utilities.format import DateUtils
from core.constants import DATEFORMAT, HEADERS, Env
from clients.nse import NSEClient
from clients.base import BaseHTTPClient


def main(ENV):
    # url = URL(DateUtils.format_date)
    url = URL(DATEFORMAT.DEFAULT)
    conn = NSEClient(url.generator, HEADERS, ENV)
    df = conn.get_data()
    print(df)


if __name__ == "__main__":
    # ENV = Env.STAGE 
    ENV = Env.PROD                      #### UNCOMMENT When deploying
    main(ENV)