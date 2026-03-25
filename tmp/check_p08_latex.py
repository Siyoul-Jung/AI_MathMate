import sqlite3
import os
import json

db_path = r"c:\AI_MathMate\backend\amc_engine\amc_factory.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT narrative FROM variants WHERE engine_id LIKE '%P08%' LIMIT 1")
row = cursor.fetchone()
if row:
    print("--- RAW NARRATIVE ---")
    print(row[0])
    print("---------------------")
else:
    print("No variant found for P08")

conn.close()
