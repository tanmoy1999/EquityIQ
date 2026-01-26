import pandas as pd
from core.constants import OUTPUT, NSE, FILEFORMAT
from utilities.format import DateUtils

class ProcessedDataExporter:
    def __init__(self, df, filename):
        self.df = df
        self.filename = filename

    def to_csv(self):
        df = self.df
        df.to_csv(OUTPUT.PROCESSED_LOCATION + "/" + self.filename + FILEFORMAT.CSV, index = False)

    def to_json(self):
        df = self.df
        df.to_json(OUTPUT.PROCESSED_LOCATION + "/" + self.filename + FILEFORMAT.JSON)

    def to_parquet(self):
        df = self.df
        df.to_parquet(OUTPUT.PROCESSED_LOCATION + "/" + self.filename + FILEFORMAT.PARQUET, index = False)

class BhavDataExporter(ProcessedDataExporter):
    def to_csv(self):
        df = self.df
        df.to_csv(OUTPUT.BHAVCOPY_LOCATION + "/" + self.filename + FILEFORMAT.CSV, index = False)

class URL:
    def __init__(self, filedate: str):
        self.filedate = filedate

    @property
    def generator(self) -> str:
        URL = "https://" + NSE.DOMAIN + "/" + NSE.PATH + "/" + NSE.FILENAME + self.filedate + NSE.FILEFORMAT
        return URL
    
    @property
    def ticker(self) -> str:
        URL = "https://" + NSE.DOMAIN + "/" + NSE.TICKER_PATH + "/" + NSE.TICKER_FILENAME + NSE.FILEFORMAT
        return URL

class FileName:
    @staticmethod
    def bhavcopy() -> str:
        return f"BhavCopy"
    
    @staticmethod
    def ChangeCapture_dt() -> str:
        return f"ChangeCapture_{DateUtils.format_date}"
    
    @staticmethod
    def ChangeCapture() -> str:
        return f"ChangeCapture"

    @staticmethod
    def delivery() -> str:
        return f"delivery_{DateUtils.format_date}.{NSE.FILEFORMAT}"

    @staticmethod
    def ChangeCol() -> str:
        return 'change_' + DateUtils.format_date
