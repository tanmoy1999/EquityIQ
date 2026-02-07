from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import logging
uri = "mongodb+srv://tanmoyworkspace_db_user:Ejevnrm3gxo2XVHe@equityiq.lysmhzc.mongodb.net/?appName=EquityIQ"

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# tanmoyworkspace_db_user Ejevnrm3gxo2XVHe