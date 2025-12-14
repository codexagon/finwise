import os

import sqlite3
from sqlite3 import Error

from datetime import datetime

DB_FILE = os.path.join(os.path.expanduser("~"), "finwise-data", "transactions.db")

# Database operations
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tables():
    create_transactions_table_query = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        date TEXT NOT NULL,
        name TEXT NOT NULL,
        amount REAL NOT NULL,
        type TEXT NOT NULL,
        category TEXT,
        description TEXT
    );
    """

    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(create_transactions_table_query)
            conn.commit()
            print("Database and tables initialized successfully.")
        except Error as e:
            print(f"Error creating tables: {e}")
        finally:
            conn.close()
    else:
        print("Cannot create tables: database connection failed.")

def add_transaction(date, amount, name, description, type, category):
    query = """
    INSERT INTO transactions (date, name, amount, type, category, description)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (date, name, amount, type, category, description))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error adding transaction: {e}")
            return None
        finally:
            print(f"Added transaction.")
            conn.close()

def get_all_transactions():
    transactions = []

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT *  FROM transactions")
            transactions = cursor.fetchall()
        except Error as e:
            print(f"Error getting all transactions: {e}")
        finally:
            conn.close()
    
    return transactions

def get_monthly_transactions():
    transactions = []

    today = datetime.now()
    first_day = today.replace(day=1).strftime("%Y-%m-%d")

    query = "SELECT * FROM transactions WHERE date >= ? ORDER BY date DESC"

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (first_day,))
            transactions = cursor.fetchall()
        except Error as e:
            print(f"Error getting monthly transactions: {e}")
        finally:
            conn.close()
    
    return transactions

def get_transactions(category, order):
    transactions = []
    sorting_order = "DESC" if order == "Descending" else "ASC"
    query = f"SELECT * FROM transactions ORDER BY {category.lower()} {sorting_order}"

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            transactions = cursor.fetchall()
        except Error as e:
            print(f"Error getting transactions: {e}")
        finally:
            conn.close()
    
    return transactions

def update_transaction(id, date, amount, name, description, type, category):
    query = """
    UPDATE transactions
    SET date = ?, amount = ?, name = ?, description = ?, type = ?, category = ?
    WHERE id = ?
    """

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (date, amount, name, description, type, category, id))
            conn.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error updating transaction (ID: {id}): {e}")
            return 0
        finally:
            print(f"Updated transaction (ID: {id}).")
            conn.close()

def delete_transaction(id):
    query = "DELETE FROM transactions WHERE id = ?"

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            conn.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error deleting transaction (ID: {id}): {e}")
            return 0
        finally:
            print(f"Deleted transaction (ID: {id}).")
            conn.close()

if __name__ == "__main__":
    create_tables()