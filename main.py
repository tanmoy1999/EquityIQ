#%%
from schemas.models import URL
from utilities.format import DateUtils
from core.constants import DATEFORMAT, HEADERS, Env, NSE_LOCAL
from clients.nse import NSEClient
from clients.base import BaseHTTPClient
from core.calculations import Col
import pandas as pd
from core.operations import DataExporter


def main(ENV):
    # url = URL(DateUtils.format_date)     #### UNCOMMENT When deploying
    url = URL(DATEFORMAT.DEFAULT)

    if ENV == Env.PROD:
        print("PROD")
        conn = NSEClient(url.generator, HEADERS, ENV)
        conn_ticker = NSEClient(url.ticker, HEADERS, ENV)
    else:
        print("STAGE")
        conn = NSEClient(NSE_LOCAL.FILENAME, HEADERS, ENV)
        conn_ticker = NSEClient(NSE_LOCAL.TICKER, HEADERS, ENV)

    df = conn.get_data()
    ticker = conn_ticker.get_data()

    ticker = ticker[ticker[' SERIES'] == "EQ"]
    ticker = ticker[['SYMBOL','NAME OF COMPANY']]
    
    df = df[df[' SERIES'] == " EQ"]
    new_col = 'change_' + DateUtils.format_date

    df1 = Col(df, new_col, ' PREV_CLOSE', ' CLOSE_PRICE')
    df2 = df1.perc_diff()
    df2 = df2[['SYMBOL',new_col]]
    print(df2)

    DataExporter(df2, "ChangeCapture").to_csv()
    DataExporter(df2, "ChangeCapture").to_json()
    DataExporter(df2, "ChangeCapture").to_parquet()

if __name__ == "__main__":
    ENV = Env.STAGE
    # ENV = Env.PROD                      #### UNCOMMENT When deploying
    main(ENV)


# %%
