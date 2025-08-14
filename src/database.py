import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from src.config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.config = Config()
        self.engine = create_engine(self.config.get_database_url())
        
    def get_connection(self):
        """Get database connection"""
        try:
            conn = psycopg2.connect(
                host=self.config.DB_HOST,
                port=self.config.DB_PORT,
                database=self.config.DB_NAME,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD
            )
            return conn
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    def execute_schema(self, schema_file_path):
        """Execute schema SQL file"""
        try:
            with open(schema_file_path, 'r') as file:
                schema_sql = file.read()
            
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(schema_sql)
            conn.commit()
            cursor.close()
            conn.close()
            logger.info("Schema executed successfully")
        except Exception as e:
            logger.error(f"Error executing schema: {e}")
            raise
    
    def insert_dataframe(self, df, table_name, if_exists='append'):
        """Insert pandas dataframe to database"""
        try:
            df.to_sql(table_name, self.engine, if_exists=if_exists, index=False)
            logger.info(f"Data inserted successfully into {table_name}")
        except Exception as e:
            logger.error(f"Error inserting data: {e}")
            raise
    
    def fetch_data(self, query, params=None):
        """Fetch data using SQL query"""
        try:
            return pd.read_sql_query(query, self.engine, params=params)
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            raise
