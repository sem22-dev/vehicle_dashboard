#!/usr/bin/env python3
import os
import sys
from src.data_processor import DataProcessor
from src.database import DatabaseManager

def main():
    # Initialize components
    data_processor = DataProcessor()
    db_manager = DatabaseManager()
    
    # Setup database schema
    try:
        db_manager.execute_schema('database/schema.sql')
        print("Database schema created successfully")
    except Exception as e:
        print(f"Schema creation error (might already exist): {e}")
    
    # Process Excel files
    data_folder = "data/raw"
    
    if not os.path.exists(data_folder):
        print(f"Data folder {data_folder} not found. Please create it and add your Excel files.")
        return
    
    print("Starting data processing...")
    result = data_processor.process_excel_files(data_folder)
    
    if result is not None:
        print(f"Successfully processed and loaded {len(result)} records")
    else:
        print("Data processing failed")

if __name__ == "__main__":
    main()
