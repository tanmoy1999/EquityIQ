from pymongo import MongoClient
import logging
from core.constants import NSE
# client = MongoClient(uri)

# # Access a specific database
# db = client['NSE']

# # Access a collection within the database
# collection = db['bhavcopy']

# # Example: Insert a document into the collection
# document = {"firstname": "John", "lastname": "Doe", "email": "tanny@example.com"}
# collection.insert_one(document)

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
