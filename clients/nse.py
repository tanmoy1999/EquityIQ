from clients.base import BaseHTTPClient
from core.constants import HEADERS, Basic
from io import StringIO
from pandas import read_csv

class NSEClient(BaseHTTPClient):
    def __init__(self, link: str, url_headers: dict):
        super().__init__(url_headers)
        self.link = link

    def get_data(self) -> dict:
        self._sleep()
        s = self.session()
        response = s.get(self.link, timeout=Basic.TIMEOUT)
        response.raise_for_status()
        if response.status_code != 200:
            raise ValueError(f"File not found. Check the link {self.link}")
        df = read_csv(StringIO(response.text))
        return df