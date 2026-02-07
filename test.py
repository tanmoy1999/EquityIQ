import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import logging
from core.constants import NSE, DatabaseConfig
from utilities.db import Database
from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne

load_dotenv(".env")
# from pymongo import MongoClient

# client = MongoClient(uri)

# # Access a specific database
# db = client['NSE']

# # Access a collection within the database
# collection = db['bhavcopy']

# # Example: Insert a document into the collection
# document = {"firstname": "John", "lastname": "Doe", "email": "tanny@example.com"}
# collection.insert_one(document)

# # result = collection.find_one({"email": "johndoe1@example.com"})
# # print(result)

df = pd.read_csv(r"storage\output\processed\ChangeCapture.csv")

db_user = os.getenv("DB_USER")
DB_KEY = os.getenv("DB_KEY")

# print(db_user, DB_KEY)
# uri = DatabaseConfig(db_user, DB_KEY).get_connection_string()
# print(uri)
# client = Database(uri)
# records = df.to_dict(orient="records")
# client.symbol_changes.deleteMany({})
# client.insert_many(records)

# print(df.to_dict(orient="records"))


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
        date_key = extract_date(col)
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