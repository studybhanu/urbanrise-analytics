import requests
from src.db_manager import get_collection

API_URL = "https://dummyjson.com/products?limit=00"

def ingest_data():
    """
    Fetches data from DummyJSON API and upserts into MongoDB.
    Returns: Status message (str)
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status() # Check for HTTP errors
        
        products = response.json().get('products', [])
        
        if not products:
            return "No products found in API response."

        collection = get_collection()
        
        # Upsert logic: Update if ID exists, Insert if not
        operations_count = 0
        for p in products:
            # We filter by 'id' and set the whole product document
            result = collection.update_one(
                {'id': p['id']}, 
                {'$set': p}, 
                upsert=True
            )
            operations_count += 1
            
        return f"Successfully processed {operations_count} products."

    except requests.exceptions.RequestException as e:
        return f"API Error: {e}"
    except Exception as e:
        return f"Database Error: {e}"