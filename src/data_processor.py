import pandas as pd
import os
import glob
from datetime import datetime
import logging
from src.database import DatabaseManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self):
        self.db_manager = DatabaseManager()
        
    def process_excel_files(self, data_folder_path):
        """Process all Excel files in the data folder"""
        excel_files = glob.glob(os.path.join(data_folder_path, "*.xlsx"))
        
        if not excel_files:
            logger.error("No Excel files found in the specified folder")
            return
        
        all_data = []
        
        for file_path in excel_files:
            try:
                # Extract vehicle category and year from filename
                filename = os.path.basename(file_path)
                parts = filename.replace('.xlsx', '').split('_')
                
                if len(parts) >= 2:
                    year = parts[0]  # e.g., "2023"
                    vehicle_category = parts[1].upper()  # e.g., "2W"
                else:
                    logger.warning(f"Unexpected filename format: {filename}")
                    continue
                
                # Read Excel file
                df = pd.read_excel(file_path)
                
                # Process the dataframe
                processed_df = self.clean_and_transform_data(df, vehicle_category, year, filename)
                
                if processed_df is not None and not processed_df.empty:
                    all_data.append(processed_df)
                    logger.info(f"Processed {filename}: {len(processed_df)} records")
                
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                continue
        
        if all_data:
            # Combine all data
            combined_df = pd.concat(all_data, ignore_index=True)
            
            # Insert into database
            self.db_manager.insert_dataframe(combined_df, 'vehicle_registrations', if_exists='append')
            logger.info(f"Successfully loaded {len(combined_df)} total records into database")
            
            return combined_df
        else:
            logger.error("No data was successfully processed")
            return None
    
    def clean_and_transform_data(self, df, vehicle_category, year, filename):
        """Clean and transform the Excel data based on actual structure"""
        try:
            logger.info(f"Processing {filename} - Shape: {df.shape}")
            
            # Skip header rows and find the data start
            # The actual data starts after the header rows
            data_start_row = 4  # Based on your log output, data starts at row 4
            df_clean = df.iloc[data_start_row:].reset_index(drop=True)
            
            # Remove rows that are completely empty
            df_clean = df_clean.dropna(how='all')
            
            if df_clean.empty:
                logger.warning(f"No data found in {filename} after cleaning")
                return None
            
            logger.info(f"Data shape after cleaning: {df_clean.shape}")
            logger.info(f"Sample cleaned data:\n{df_clean.head()}")
            
            processed_records = []
            
            # Process each row
            for idx, row in df_clean.iterrows():
                try:
                    # Skip rows with no meaningful data
                    if pd.isna(row.iloc[0]) or str(row.iloc[0]).strip() == '':
                        continue
                    
                    # Get the serial number (first column)
                    serial_no = str(row.iloc[0]).strip()
                    
                    # Skip if it's not a valid serial number
                    if not serial_no.isdigit():
                        continue
                    
                    # Get vehicle type name (second column)
                    if len(row) > 1 and pd.notna(row.iloc[1]):
                        vehicle_type = str(row.iloc[1]).strip()
                    else:
                        continue
                    
                    # Get the total registrations (last column with data)
                    total_registrations = 0
                    
                    # Look for the TOTAL column or the last numeric column
                    for col_idx in range(len(row)-1, -1, -1):
                        val = row.iloc[col_idx]
                        if pd.notna(val):
                            # Handle comma-separated numbers
                            val_str = str(val).replace(',', '').strip()
                            if val_str.isdigit():
                                total_registrations = int(val_str)
                                break
                    
                    # Skip if no valid registration count found
                    if total_registrations <= 0:
                        continue
                    
                    # Create registration date (middle of the year for analytics)
                    registration_date = f"{year}-06-15"
                    
                    # Use vehicle type as manufacturer for this data structure
                    # This makes sense because your data is grouped by vehicle types, not manufacturers
                    manufacturer = vehicle_type.title()
                    
                    # Create record
                    record = {
                        'registration_date': registration_date,
                        'vehicle_category': vehicle_category,
                        'manufacturer': manufacturer,  # Using vehicle type as manufacturer
                        'state': 'ALL INDIA',  # Since this appears to be aggregate data
                        'district': 'ALL DISTRICTS',
                        'rto_code': 'ALL_RTO',
                        'registrations_count': total_registrations
                    }
                    
                    processed_records.append(record)
                    logger.debug(f"Added record: {vehicle_type} -> {total_registrations}")
                    
                except Exception as e:
                    logger.debug(f"Error processing row {idx}: {e}")
                    continue
            
            if not processed_records:
                logger.warning(f"No valid records extracted from {filename}")
                return None
            
            processed_df = pd.DataFrame(processed_records)
            logger.info(f"Successfully extracted {len(processed_df)} records from {filename}")
            
            return processed_df
            
        except Exception as e:
            logger.error(f"Error in clean_and_transform_data for {filename}: {e}")
            return None
    
    def calculate_growth_metrics(self):
        """Calculate YoY and QoQ growth metrics"""
        try:
            # YoY Growth by Category
            yoy_query = """
            WITH yearly_data AS (
                SELECT 
                    EXTRACT(YEAR FROM registration_date) as year,
                    vehicle_category,
                    SUM(registrations_count) as total_registrations
                FROM vehicle_registrations 
                GROUP BY EXTRACT(YEAR FROM registration_date), vehicle_category
            ),
            yoy_growth AS (
                SELECT 
                    year,
                    vehicle_category,
                    total_registrations,
                    LAG(total_registrations) OVER (PARTITION BY vehicle_category ORDER BY year) as prev_year_registrations,
                    CASE 
                        WHEN LAG(total_registrations) OVER (PARTITION BY vehicle_category ORDER BY year) IS NOT NULL 
                        THEN ROUND(((total_registrations - LAG(total_registrations) OVER (PARTITION BY vehicle_category ORDER BY year)) * 100.0 / 
                                   LAG(total_registrations) OVER (PARTITION BY vehicle_category ORDER BY year)), 2)
                        ELSE NULL 
                    END as yoy_growth_percent
                FROM yearly_data
            )
            SELECT * FROM yoy_growth WHERE yoy_growth_percent IS NOT NULL
            ORDER BY vehicle_category, year;
            """
            
            # QoQ Growth by Category
            qoq_query = """
            WITH quarterly_data AS (
                SELECT 
                    EXTRACT(YEAR FROM registration_date) as year,
                    EXTRACT(QUARTER FROM registration_date) as quarter,
                    vehicle_category,
                    SUM(registrations_count) as total_registrations
                FROM vehicle_registrations 
                GROUP BY EXTRACT(YEAR FROM registration_date), EXTRACT(QUARTER FROM registration_date), vehicle_category
            ),
            qoq_growth AS (
                SELECT 
                    year,
                    quarter,
                    vehicle_category,
                    total_registrations,
                    LAG(total_registrations) OVER (PARTITION BY vehicle_category ORDER BY year, quarter) as prev_quarter_registrations,
                    CASE 
                        WHEN LAG(total_registrations) OVER (PARTITION BY vehicle_category ORDER BY year, quarter) IS NOT NULL 
                        THEN ROUND(((total_registrations - LAG(total_registrations) OVER (PARTITION BY vehicle_category ORDER BY year, quarter)) * 100.0 / 
                                   LAG(total_registrations) OVER (PARTITION BY vehicle_category ORDER BY year, quarter)), 2)
                        ELSE NULL 
                    END as qoq_growth_percent
                FROM quarterly_data
            )
            SELECT * FROM qoq_growth WHERE qoq_growth_percent IS NOT NULL
            ORDER BY vehicle_category, year, quarter;
            """
            
            yoy_data = self.db_manager.fetch_data(yoy_query)
            qoq_data = self.db_manager.fetch_data(qoq_query)
            
            return yoy_data, qoq_data
            
        except Exception as e:
            logger.error(f"Error calculating growth metrics: {e}")
            return None, None
