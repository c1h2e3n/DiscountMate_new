import json
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import List, Dict, Any
from datetime import datetime
import os


class DiscountMateDB:
    def __init__(self, config_path: str):
    # Check if the config file exists
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        # Read the configuration file
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        
        connection_string = config['connection_string']
        database_name = config['database_name']
        
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection: Collection = self.db.transactions

    def write_data(self, data: List[Dict[str, Any]]) -> None:
        if not isinstance(data, list):
            raise TypeError("Data should be a list of dictionaries.")
        if not all(isinstance(item, dict) for item in data):
            raise TypeError("Each item in the data list should be a dictionary.")
        
        # Add timestamp to each document
        current_time = datetime.utcnow()
        for item in data:
            item['timestamp'] = current_time
        
        self.collection.insert_many(data)

    def read_data(self, query: Dict[str, Any] = {}, limit: int = 10) -> List[Dict[str, Any]]:
        return list(self.collection.find(query).limit(limit))

    def close_connection(self) -> None:
        self.client.close()

# Example usage:
if __name__ == "__main__":
    config_path = os.path.abspath("db-config.json")    
    print(f"Config file path: {config_path}")
     
    db = DiscountMateDB(config_path)
    
    # Sample data
    sample_data = [
        {
            "productcode": "12345",
            "category_name": "Electronics",
            "name": "Smartphone",
            "best_price": 299.99,
            "best_unitprice": 299.99,
            "itemprice": 349.99,
            "unitprice": 349.99,
            "price_was": 399.99,
            "specialtext": "10% off",
            "complexpromo": None,
            "link": "http://example.com/product/12345"
        },
        # Add more items as needed
    ]
    
    # Write data to the collection
    db.write_data(sample_data)
    
    # Read data from the collection
    data = db.read_data({}, 5)
    for item in data:
        print(item)
    
    # Close the connection
    db.close_connection()
