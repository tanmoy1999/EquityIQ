from enum import Enum

class NSE:
    DOMAIN = "nsearchives.nseindia.com"
    PATH = "products/content"
    FILENAME = "sec_bhavdata_full_"
    FILEFORMAT = ".csv"
    TICKER_PATH = "content/equities"
    TICKER_FILENAME = "EQUITY_L"
    EQUITY = "EQ"

class FILEFORMAT:
    CSV = ".csv"
    PARQUET = ".parquet"
    JSON = ".json"

class NSE_LOCAL(str, Enum):
    FILENAME = r"storage\output\bhavdata\sec_bhavdata_full_13012026.csv"
    TICKER = r"storage\ticker\EQUITY_L.csv"
    PROCESSED_LOCATION = 'storage/output/processed'

class OUTPUT:
    PROCESSED_LOCATION = r"storage\output\processed"
    BHAVCOPY_LOCATION = 'storage/output/bhavdata'


class DATEFORMAT:
    DATE_STANDARD = "%d%m%Y"
    DATETIME_STANDARD = "%d%m%Y%H%M%S"
    DEFAULT = "23012026"

class Basic:
    TIMEOUT = 20

class Env(str, Enum):
    STAGE = "STAGE"
    PROD = "PROD"