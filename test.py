import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import logging
from core.constants import NSE, DatabaseConfig
from utilities.db import Database
from utilities.format import DateUtils
from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne

load_dotenv(".env")

df = pd.read_csv(r"storage\output\processed\ChangeCapture.csv")

db_user = os.getenv("DB_USER")
DB_KEY = os.getenv("DB_KEY")


# This will go to utilities/db.py and will be used in main.py to insert the final result into MongoDB
def extract_date(col: str) -> str:
    # change_07022026_x → 2026-02-07
    date_part = col.replace("change_", "").split("_")[0]
    return f"{date_part[4:8]}-{date_part[2:4]}-{date_part[0:2]}"


uri = DatabaseConfig(db_user, DB_KEY).get_connection_string()
client = MongoClient(uri)
collection = client.NSE.bhav

collection.create_index("symbol", unique=True)

date_cols = [c for c in df.columns if c.startswith("change_")]

bulk_ops = []

for _, row in df.iterrows():
    updates = {}

    for col in date_cols:
        # date_key = extract_date(col)
        date_key = DateUtils.extract_date(col)
        updates[f"changes.{date_key}"] = row[col]

    bulk_ops.append(
        UpdateOne(
            {"symbol": row["SYMBOL"]},
            {
                "$set": updates,
                "$setOnInsert": {"symbol": row["SYMBOL"]},
                "$currentDate": {"last_updated": True}
            },
            upsert=True
        )
    )

if bulk_ops:
    collection.bulk_write(bulk_ops)