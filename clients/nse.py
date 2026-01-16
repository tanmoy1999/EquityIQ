from typing import Literal
from clients.base import BaseHTTPClient
from core.constants import HEADERS, Basic, Env
from io import StringIO
from pandas import read_csv

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
            print("STAGE")
            df = read_csv(r'storage\output\bhavdata\sec_bhavdata_full_13012026.csv')
            return df