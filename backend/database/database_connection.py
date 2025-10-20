### --------- External Imports --------- ###
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

### --------- Load Env Variables --------- ###
load_dotenv()


### --------- Database Connection --------- ###
def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg2.connect(
            os.getenv("DATABASE_URL"), cursor_factory=RealDictCursor
        )
        return conn

    except Exception as e:
        print(f"Database connection error: {e}")
        raise
