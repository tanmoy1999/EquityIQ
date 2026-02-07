#%%

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
uri = "mongodb+srv://mongodb:mongodb@cluster0.98f2p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# %%
from pymongo import MongoClient

client = MongoClient(uri)

# Access a specific database
db = client['db1']

# Access a collection within the database
collection = db['stockchange']

# Example: Insert a document into the collection
document = {"firstname": "John", "lastname": "Doe", "email": "johndoe1@example.com"}
collection.insert_one(document)

# %%
# Example: Query a document
result = collection.find_one({"email": "johndoe@example.com"})
print(result)
# %%

documents = list(collection.find())
documents
# %%
df = pd.DataFrame(documents)

df
# %%
from pymongo import MongoClient

client = MongoClient(uri)

# Access a specific database
db = client['db1']

# Access a collection within the database
collection = db['collec1']

# Define the data
data = {
    "SYMBOL": ["1018GS2026", "20MICRONS", "21STCENMGM", "360ONE", "3IINFOLTD"],
    "SERIES": ["GS", "EQ", "BE", "EQ", "EQ"],
    "DATE1": ["24-Jan-2025"] * 5,
    "PREV_CLOSE": [109.95, 208.78, 86.24, 1141.45, 27.71],
    "OPEN_PRICE": [108.25, 208.78, 87.9, 1140.65, 28.05],
    "HIGH_PRICE": [109.6, 211, 87.9, 1155, 28.05],
    "LOW_PRICE": [108.25, 200, 84.51, 1101, 27],
    "LAST_PRICE": [109.6, 200.01, 84.51, 1128, 27.02],
    "CLOSE_PRICE": [109.6, 201.55, 84.51, 1127.4, 27.06],
    "AVG_PRICE": [109.59, 204.56, 85.62, 1125.15, 27.27],
    "TTL_TRD_QNTY": [2020, 179701, 4295, 297675, 206388],
    "TURNOVER_LACS": [2.21, 367.59, 3.68, 3349.29, 56.29],
    "NO_OF_TRADES": [2, 4438, 62, 21569, 1750],
    "DELIV_QTY": ["2020", "87400", "-", "154636", "99144"],
    "DELIV_PER": [100, 48.64, "-", 51.95, 48.04],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Convert DataFrame to a list of dictionaries (MongoDB format)
data_dict = df.to_dict("records")

# Insert data into MongoDB
collection.insert_many(data_dict)

print("Data inserted into MongoDB successfully!")

#%%

documents = list(collection.find())
documents
# %%
result = collection.find({"SYMBOL": "3IINFOLTD"})
print(result)

#%%

import pandas as pd

# Load the CSV file into a DataFrame
# Replace 'your_file.csv' with your actual file path
df = pd.read_csv("sec_bhavdata_full_23012025.csv")

# Convert DataFrame to a list of dictionaries (JSON-like structure)
json_result = df.to_dict("records")

# Print the JSON result
import json
print(json.dumps(json_result, indent=4))

# Save JSON to a file (optional)
with open("output.json", "w") as json_file:
    json.dump(json_result, json_file, indent=4)

print("JSON saved successfully!")

#%%

for i in range(0,100):
    data = json_result[i]
    collection.insert_one(data)
    print("inserted ",i)

#%%

import pandas as pd

# URL of the CSV file
url = "https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_23012025.csv"  # Replace with the actual URL

# Read the CSV from the URL into a Pandas DataFrame
df = pd.read_csv(url)

# Display the DataFrame
print(df.head())


#%%
import pandas as pd
import statsmodels.api as sm

# Create DataFrame
data = pd.DataFrame({
    "Study_Hours": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Sleep_Hours": [8, 7, 6, 6, 5, 5, 4, 4, 3, 3],
    "Junk_Food": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],  # 1 = Eats junk food, 0 = No junk food
    "Grades": [50, 55, 60, 63, 70, 75, 80, 85, 90, 95]
})

# Define X (independent variables) and y (dependent variable)
X = data[["Study_Hours", "Sleep_Hours", "Junk_Food"]]
y = data["Grades"]

# Add constant (intercept)
X = sm.add_constant(X)

# Train model
model = sm.OLS(y, X).fit()

# Print p-values
print(model.pvalues)

# %%
