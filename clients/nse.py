from typing import Literal
from clients.base import BaseHTTPClient
from core.constants import Basic, Env
from io import StringIO
from pandas import read_csv
import requests
import csv
import io

class NSEClient(BaseHTTPClient):
    def __init__(self, link: str, url_headers: dict, env: Literal["LOCAL", "PROD"]):
        super().__init__(url_headers)
        self.link = link
        self.env = env

    def get_data(self):
        if self.env == Env.PROD:
            self._sleep()
            s = self.session()
            response = s.get(self.link, timeout=Basic.TIMEOUT)
            response.raise_for_status()
            if response.status_code != 200:
                raise ValueError(f"File not found. Check the link {self.link}")
            df = read_csv(StringIO(response.text))
            return df
        else:
            df = read_csv(self.link)
            return df
        
    def get_file(self):
        s = self.session()
        response = s.get(self.link, timeout=Basic.TIMEOUT, headers=self.url_headers, stream=True)
        response.raise_for_status()
        text_stream = io.TextIOWrapper(response.raw, encoding="utf-8")
        reader = csv.DictReader(text_stream)
        return reader
    
class Report:
    def __init__(self, location: str):
        self.location = location

    @property
    def read(self):
        df = read_csv(self.location)
        return df
