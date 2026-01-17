import pandas as pd
from core.constants import OUTPUT, NSE, FILEFORMAT

class DataExporter:
    def __init__(self, df, filename):
        self.df = df
        self.filename = filename

    def to_csv(self):
        df = self.df
        df.to_csv(OUTPUT.LOCATION + "/" + self.filename + FILEFORMAT.CSV, index = False)

    def to_json(self):
        df = self.df
        df.to_json(OUTPUT.LOCATION + "/" + self.filename + FILEFORMAT.JSON)

    def to_parquet(self):
        df = self.df
        df.to_parquet(OUTPUT.LOCATION + "/" + self.filename + FILEFORMAT.PARQUET, index = False)