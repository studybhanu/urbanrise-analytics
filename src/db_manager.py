import pymongo
import pandas as pd
import os

# Configuration
DB_URI = os.getenv("DB_URI", "mongodb://localhost:27017/")
DB_NAME = "urbanrise_analytics"
COLLECTION_NAME = "products"


def get_collection():
    """Establishes connection and returns the MongoDB collection."""
    client = pymongo.MongoClient(DB_URI)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]

def fetch_data_as_df():
    """Fetches all data from MongoDB and converts it to a Pandas DataFrame."""
    collection = get_collection()
    data = list(collection.find({}, {'_id': 0})) # Exclude Mongo ID for cleaner DF
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)