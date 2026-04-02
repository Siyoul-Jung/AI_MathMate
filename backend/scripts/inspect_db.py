import sqlite3
import os

# Correct path relative to project root
db_path = 'backend/amc_engine/amc_factory.db'

if not os.path.exists(db_path):
    print(f"Error: Database not found at {db_path}")
    sys.exit(1)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Get tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()

print(f"Tables: {[t[0] for t in tables]}")

for table in tables:
    table_name = table[0]
    print(f"\n--- {table_name} ---")
    cur.execute(f"PRAGMA table_info({table_name});")
    info = cur.fetchall()
    for col in info:
        print(f"  {col[1]} ({col[2]})")

conn.close()
