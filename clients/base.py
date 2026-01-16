import time
import requests
import random

class BaseHTTPClient:
    def __init__(self, url_headers: dict):
        self.url_headers = url_headers
    
    def session(self):
        client = requests.Session()
        client.headers.update(self.url_headers)
        return client

    def _sleep(self) -> None:
        print("sleeping... 4s")
        time.sleep(4)
