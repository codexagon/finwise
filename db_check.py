import sqlite3, os
from sqlite3 import Error

db_file_path = os.path.join(os.path.expanduser("~"), "finwise-data", "transactions.db")

conn = None
try:
    conn = sqlite3.connect(db_file_path)
except Error as e:
    print(f"Error: unable to connect to database: {e}")
    exit()

cursor = conn.cursor()

cursor.execute("SELECT * FROM transactions")

transactions = cursor.fetchall()

for t in transactions:
    print(f"{t[0]}     {t[1]}     {t[2]}     {t[3]}     {t[4]}     {t[5]}     {t[6]}")

conn.close()