### --------- External Imports --------- ###
import os
import psycopg2
from dotenv import load_dotenv

### --------- Load Env Variables --------- ###
load_dotenv()


### --------- Database Initialization --------- ###
def init_database():
    conn = None
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cursor = conn.cursor()

        # Create table
        table_query = """
        CREATE TABLE IF NOT EXISTS text_analysis_results (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL,
            sentiment_label VARCHAR(10) NOT NULL,
            confidence_score DECIMAL(5, 4) NOT NULL,
            positive_score DECIMAL(5, 4),
            negative_score DECIMAL(5, 4),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """

        # Create table if it doesn't exist
        cursor.execute(table_query)
        conn.commit()

        print("Database initialized successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error initializing database: {error}")

    finally:
        # Close the cursor and connection
        if conn:
            cursor.close()
            conn.close()
