### --------- External Imports --------- ###
from datetime import datetime
from typing import List, Dict, Any, Optional


### --------- Internal Imports --------- ###
from database.database_connection import get_db_connection


### --------- Database Operations --------- ###
# Save analysis to database
def save_analysis(
    text: str,
    label: str,
    confidence: float,
    positive_score: Optional[float] = None,
    negative_score: Optional[float] = None,
) -> Dict[str, Any]:
    """Save analysis to database"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Calculate scores if not provided
        if positive_score is None or negative_score is None:
            if label.upper() == "POSITIVE":
                positive_score = confidence
                negative_score = 1 - confidence
            else:
                negative_score = confidence
                positive_score = 1 - confidence

        insert_query = """
        INSERT INTO text_analysis_results (text, sentiment_label, confidence_score, positive_score, negative_score, created_at) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id, text, sentiment_label, confidence_score, positive_score, negative_score, created_at; 
        """

        cursor.execute(
            insert_query,
            (
                text,
                label.upper(),
                confidence,
                positive_score,
                negative_score,
                datetime.now(),
            ),
        )
        result = cursor.fetchone()
        conn.commit()

        # Return analysis as dictionary
        if result:
            return dict(result)
        else:
            return {}

    except Exception as e:
        print(f"Error saving analysis: {e}")
        raise

    finally:
        if conn:
            cursor.close()
            conn.close()


# Get all analyses from database
def get_all_analyses(limit: int = 20) -> List[Dict[str, Any]]:
    """Get all analyses from database"""
    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        select_query = """
        SELECT id, text, sentiment_label, confidence_score, positive_score, negative_score, created_at
        FROM text_analysis_results
        ORDER BY created_at DESC
        LIMIT %s;
        """

        cursor.execute(select_query, (limit,))
        results = cursor.fetchall()

        return [dict(row) for row in results]

    except Exception as e:
        print(f"Error fetching analyses: {e}")
        return []

    finally:
        if conn:
            cursor.close()
            conn.close()


# Get single analysis by ID
def get_single_analysis(analysis_id: int) -> Dict[str, Any]:
    """Get single analysis by ID"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        select_query = """
        SELECT id, text, sentiment_label, confidence_score, positive_score, negative_score, created_at
        FROM text_analysis_results
        WHERE id=%s;
        """

        cursor.execute(select_query, (analysis_id,))
        result = cursor.fetchone()

        if result:
            return dict(result)
        else:
            return {}

    except Exception as e:
        print(f"Error fetching analysis: {e}")
        return {}

    finally:
        if conn:
            cursor.close()
            conn.close()


def search_analyses(search_text: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Search analyses by text content"""
    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        search_query = """
        SELECT id, text, sentiment_label, confidence_score, positive_score, negative_score, created_at
        FROM text_analysis_results
        WHERE text ILIKE %s
        ORDER BY created_at DESC
        LIMIT %s
        """

        cursor.execute(search_query, (f"%{search_text}%", limit))
        results = cursor.fetchall()

        if results:
            return [dict(row) for row in results]
        else:
            return []

    except Exception as e:
        print(f"Error searching analyses: {e}")
        return []

    finally:
        if conn:
            cursor.close()
            conn.close()


def delete_analysis(analysis_id: int) -> bool:
    """Delete specific analysis by ID"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        delete_query = "DELETE FROM text_analysis_results WHERE id = %s;"
        cursor.execute(delete_query, (analysis_id,))
        conn.commit()

        return cursor.rowcount > 0

    except Exception as e:
        print(f"Error deleting analysis: {e}")
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()
