from utilities.format import DateUtils
from core.constants import DATEFORMAT, Env, NSE_LOCAL, NSE, FILEFORMAT, OUTPUT
from clients.nse import NSEClient, Report
from clients.base import BaseHTTPClient
from core.calculations import Col
import pandas as pd
from core.operations import ProcessedDataExporter,BhavDataExporter, URL, FileName
from schemas.models import Ticker, BhavData
from utilities.logging import get_logger

logger = get_logger(__name__)

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

def main(ENV) -> None:
    # url = URL(DateUtils.format_date)     #### UNCOMMENT When deploying
    url = URL(DATEFORMAT.DEFAULT)

    if ENV == Env.PROD:
        logger.info("Running in PROD environment")
        logger.debug(f"URL: {url.generator}")
        conn = NSEClient(url.generator, HEADERS, ENV)
        logger.debug(f"URL: {url.ticker}")
        conn_ticker = NSEClient(url.ticker, HEADERS, ENV)
    else:
        logger.info("Running in STAGE environment")
        conn = NSEClient(NSE_LOCAL.FILENAME, HEADERS, ENV)
        conn_ticker = NSEClient(NSE_LOCAL.TICKER, HEADERS, ENV)

    try:
        df = conn.get_data()
        BhavDataExporter(df,NSE.FILENAME + DateUtils.format_date).to_csv()
        logger.debug("Fetched & Exported bhavcopy rows: %d", len(df))
        ticker = conn_ticker.get_data()
    except Exception as e:
        logger.exception("Failed to fetch bhavcopy data from NSE")
        raise RuntimeError("Failed to fetch bhavcopy data from NSE") from e

    ticker = ticker[ticker[Ticker.SYMBOL] == NSE.EQUITY]
    ticker = ticker[[Ticker.SYMBOL,Ticker.NAME_OF_COMPANY]]
    
    df_fil_eq = df[df[Ticker.SERIES] == NSE.EQUITY]
    new_col = FileName.ChangeCol()

    df_close = Col(df_fil_eq, new_col, BhavData.PREV_CLOSE, BhavData.CLOSE_PRICE)
    df_cc = df_close.perc_diff()
    df_cc = df_cc[[BhavData.SYMBOL,new_col]]
    
    try:
        logger.debug("Reading last report.")
        lastReport =  Report(NSE_LOCAL.PROCESSED_LOCATION + "/" + FileName.ChangeCapture() + FILEFORMAT.CSV).load() # Read last Master file ChangeCapture.csv
    except FileNotFoundError as e:
        logger.exception("Last Report ChangeCapture.csv not found")
        raise FileNotFoundError("Last Report ChangeCapture.csv not found") from e

    ProcessedDataExporter(df_cc, FileName.ChangeCapture()).to_csv() #ChangeCapture.csv
    
    result = df_cc.merge(
        lastReport,
        on=BhavData.SYMBOL,
        how="left"
    )

    ProcessedDataExporter(result, FileName.ChangeCapture()).to_csv() #ChangeCapture.csv
    logger.info("Final file merged and exported.")

if __name__ == "__main__":
    # ENV = Env.STAGE
    ENV = Env.PROD                      #### UNCOMMENT When deploying
    main(ENV)
