class NSE:
    DOMAIN = "nsearchives.nseindia.com"
    PATH = "products/content"
    FILENAME = "sec_bhavdata_full_"
    FILEFORMAT = ".csv"

class DATEFORMAT:
    DATE_STANDARD = "%d%m%Y"
    DATETIME_STANDARD = "%d%m%Y%H%M%S"
    DEFAULT = "13012026"

class Basic:
    TIMEOUT = 20

class Env:
    STAGE = "STAGE"
    PROD = "PROD"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/csv,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.nseindia.com/",
    "Connection": "keep-alive",
    "DNT": "1",                       # Do Not Track (browser-like)
    "Upgrade-Insecure-Requests": "1"
}