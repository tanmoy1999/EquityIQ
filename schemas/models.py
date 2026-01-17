from core.constants import NSE

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


    
