from pymongo import MongoClient, UpdateOne
import logging
from core.constants import NSE
from utilities.format import DateUtils
from schemas.models import BhavData, DBkey, AUDITCOLS

class Database:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client[NSE.NSE]
        self.collection = self.db[NSE.BHAVCOPY]

    def insert_one(self, document):
        try:
            self.collection.insert_one(document)
            logging.info("Document inserted successfully.")
        except Exception as e:
            logging.exception(f"Error inserting document: {e}")

    def insert_many(self, documents):
        try:
            self.collection.insert_many(documents)
            logging.info("Documents inserted successfully.")
        except Exception as e:
            logging.exception(f"Error inserting documents: {e}")

    def find_document(self, query):
        try:
            result = self.collection.find_one(query)
            logging.info("Document found successfully.")
            return result
        except Exception as e:
            logging.exception(f"Error finding document: {e}")
            return None

    def bulk_upsert(self, df, date_cols):
        try:
            bulk_ops = []
            
            self.collection.create_index(DBkey.SYMBOL_key, unique=True)
            
            for _, row in df.iterrows():
                updates = {}
                
                for col in date_cols:
                    date_key = DateUtils.extract_date(col)
                    updates[f"changes.{date_key}"] = row[col]
                
                bulk_ops.append(
                    UpdateOne(
                        {DBkey.SYMBOL_key: row[BhavData.SYMBOL]},
                        {
                            "$set": updates,
                            "$setOnInsert": {DBkey.SYMBOL_key: row[BhavData.SYMBOL]},
                            "$currentDate": {AUDITCOLS.LAST_UPDATED: True}
                        },
                        upsert=True
                    )
                )
            
            if bulk_ops:
                self.collection.bulk_write(bulk_ops)
                logging.info("Bulk upsert completed successfully.")
        except Exception as e:
            logging.exception(f"Error in bulk upsert: {e}")
