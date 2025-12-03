import sqlite3
from sqlite3 import Error

conn = sqlite3.connect("finance_tracker.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM transactions")

transactions = cursor.fetchall()

for t in transactions:
    print(f"{t[0]}     {t[1]}     {t[2]}     {t[3]}     {t[4]}     {t[5]}     {t[6]}")

conn.close()