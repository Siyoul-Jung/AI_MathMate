import sqlite3
import os

db_path = r"c:\AI_MathMate\backend\amc_engine\amc_factory.db"

if not os.path.exists(db_path):
    print(f"Error: Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("--- Variant Counts by Problem ID ---")
cursor.execute("SELECT engine_id, COUNT(*) FROM variants GROUP BY engine_id")
rows = cursor.fetchall()
for row in rows:
    print(f"{row[0]}: {row[1]} variants")

print("\n--- Summary ---")
cursor.execute("SELECT COUNT(*) FROM variants")
total = cursor.fetchone()[0]
print(f"Total variants: {total}")

conn.close()
