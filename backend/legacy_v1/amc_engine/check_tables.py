import sqlite3

DB_PATH = r'c:\AI_MathMate\amc_engine\datasets\2025\AIME1\AIME1_Problems.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tables in AIME1_Problems.db:", cursor.fetchall())
conn.close()
